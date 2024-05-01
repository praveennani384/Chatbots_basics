import os.path
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('wordnet')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load or initialize data
data_file = 'data.json'
if os.path.exists(data_file):
    with open(data_file, 'r') as file:
        data = json.load(file)
else:
    data = {'qa_pairs': []}

# Preprocess data
corpus = []
responses = []

for qa_pair in data['qa_pairs']:
    corpus.append(qa_pair['question'])
    if 'answer' in qa_pair:
        responses.append(qa_pair['answer'])
    else:
        responses.append(None)

# Initialize CountVectorizer
vectorizer = CountVectorizer()

# Function to preprocess text
def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return ' '.join(lemmatized_tokens)

# Function to get response from chatbot
def get_response(user_input):
    # Fit the CountVectorizer to the corpus
    X = vectorizer.fit_transform(corpus)
    
    # Reinitialize CountVectorizer and transform the user input
    input_vectorizer = CountVectorizer(vocabulary=vectorizer.get_feature_names_out())
    input_vector = input_vectorizer.fit_transform([preprocess_text(user_input)])

    # Calculate cosine similarities between input and known patterns
    similarities = cosine_similarity(input_vector, X)
    max_similarity_index = np.argmax(similarities)
    
    if similarities[0][max_similarity_index] < 0.2: # Threshold for similarity
        # If the input is not similar to any known question, return "I don't understand"
        return None, None, None
    else:
        # Return the response corresponding to the most similar question
        return responses[max_similarity_index], corpus[max_similarity_index], max_similarity_index


# Function to handle "change:" functionality
def change_answer(user_input):
    question_to_change = user_input[len('change:'):].strip()
    # Use difflib to find the closest match to the question provided by the user
    closest_matches = get_close_matches(question_to_change, corpus, n=1, cutoff=0.6)
    if closest_matches:
        closest_match = closest_matches[0]
        print(f"Chatbot: Did you mean '{closest_match}'? (yes/no)")
        confirmation = input("You: ").strip().lower()
        if confirmation == 'yes':
            new_answer = input("Enter the new answer: ").strip()  # Get the new answer
            # Update the existing answer
            index = corpus.index(closest_match)
            responses[index] = new_answer
            if closest_match in [qa['question'] for qa in data['qa_pairs']]:
                data['qa_pairs'][index]['answer'] = new_answer
            else:
                data['qa_pairs'].append({'question': closest_match, 'answer': new_answer})
            print("Chatbot: Answer changed successfully.")
            # Save updated data to file
            with open(data_file, 'w') as file:
                json.dump(data, file, indent=4)
        elif confirmation == 'no':
            print("Chatbot: Please provide the correct question and its answer.")
            new_question = input("Enter the new question: ").strip()
            new_answer = input("Enter the answer: ").strip()
            # Add the new question-answer pair to the dataset
            data['qa_pairs'].append({'question': new_question, 'answer': new_answer})
            corpus.append(new_question)
            responses.append(new_answer)
            # Fit the CountVectorizer to the updated corpus
            X = vectorizer.fit_transform(corpus)
            # Save updated data to file
            with open(data_file, 'w') as file:
                json.dump(data, file, indent=4)
            print("Chatbot: New question and answer added to the dataset.")
        else:
            print("Chatbot: Invalid input. Please respond with 'yes' or 'no'.")
    else:
        print("Chatbot: No similar question found in the dataset. Please provide a new question and its answer.")
        new_question = input("Enter the new question: ").strip()
        new_answer = input("Enter the answer: ").strip()
        # Add the new question-answer pair to the dataset
        data['qa_pairs'].append({'question': new_question, 'answer': new_answer})
        corpus.append(new_question)
        responses.append(new_answer)
        # Fit the CountVectorizer to the updated corpus
        X = vectorizer.fit_transform(corpus)
        # Save updated data to file
        with open(data_file, 'w') as file:
            json.dump(data, file, indent=4)
        print("Chatbot: New question and answer added to the dataset.")

# Main loop
while True:
    user_input = input("You: ").strip()  # Remove leading and trailing whitespace
    if user_input.lower() == 'exit':
        break
    elif user_input.startswith('change:'):
        change_answer(user_input)
    else:
        # Get the response based on user input
        response, closest_question, max_similarity_index = get_response(user_input)
        if response:
            print("Chatbot:", response)
        else:
            print("Chatbot: I'm sorry, I don't know the answer to that.")
            if closest_question:
                print(f"Chatbot: Did you mean '{closest_question}'? (yes/no)")
                confirmation = input("You: ").strip().lower()
                if confirmation == 'yes':
                    print("Chatbot: Please provide the correct response.")
                    new_response = input("You: ").strip()
                    print("Chatbot: Thank you for teaching me!")
                    
                    # Record user input and response to data
                    data['qa_pairs'].append({
                        'question': user_input,
                        'answer': new_response
                    })
                    
                    # Update corpus and re-fit CountVectorizer
                    corpus.append(user_input)
                    responses.append(new_response)
                    # Fit the CountVectorizer to the updated corpus
                    X = vectorizer.fit_transform(corpus)
                        
                    # Save updated data to file
                    with open(data_file, 'w') as file:
                        json.dump(data, file, indent=4)
                else:
                    print("Chatbot: Okay, let's try again.")
            else:
                print("Chatbot: Please provide the correct question and its answer.")
                new_question = input("Enter the new question: ").strip()
                new_answer = input("Enter the answer: ").strip()
                # Add the new question-answer pair to the dataset
                data['qa_pairs'].append({'question': new_question, 'answer': new_answer})
                corpus.append(new_question)
                responses.append(new_answer)
                # Fit the CountVectorizer to the updated corpus
                X = vectorizer.fit_transform(corpus)
                # Save updated data to file
                with open(data_file, 'w') as file:
                    json.dump(data, file, indent=4)
                print("Chatbot: New question and answer added to the dataset.")
