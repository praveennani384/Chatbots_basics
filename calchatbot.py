import os.path
import json
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re  # Import the regular expressions module

#Addition: "CAL 10 + 5"
#Subtraction: "CAL 10 - 5"
#Multiplication: "CAL 10 * 5"
#Division: "CAL 10 / 5"
#Exponentiation: "CAL 2 ** 3" (which represents 2 raised to the power of 3)

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
# Preprocess data
corpus = []
responses = []

for qa_pair in data['qa_pairs']:
    corpus.append(qa_pair['question'])
    if 'answer' in qa_pair:
        responses.append(qa_pair['answer'])  # Check if 'answer' key exists
    else:
        responses.append("")  # If 'answer' key is missing, append an empty string

# Initialize CountVectorizer and fit_transform the corpus
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)

# Function to preprocess text
def preprocess_text(text):
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens]
    return ' '.join(lemmatized_tokens)

# Function to get response from chatbot
def get_response(user_input):
    preprocessed_input = preprocess_text(user_input)
    input_vector = vectorizer.transform([preprocessed_input])

    # Calculate cosine similarities between input and known patterns
    similarities = cosine_similarity(input_vector, X)
    max_similarity_index = np.argmax(similarities)
    
    if similarities[0][max_similarity_index] >= 0.2:  # Adjusted threshold condition
        # If the similarity is above the threshold, return the response
        return responses[max_similarity_index]
    else:
        # If the similarity is below the threshold, return None
        return None


# Function to evaluate calculator expressions
def evaluate_expression(expression):
    try:
        result = eval(expression)  # Evaluate the expression
        return str(result)  # Convert result to string
    except Exception as e:
        return "Error: " + str(e)  # Return error message if expression is invalid

# Main loop
while True:
    user_input = input("You: ").strip()  # Remove leading and trailing whitespace
    if user_input.lower() == 'exit':
        break
    else:
        # Check if the input is a request to use the calculator feature
        if user_input.startswith('CAL') or user_input.startswith('cal'): # Modify the condition to check for "CAL" prefix
            expression = user_input[3:].strip()  # Extract the expression after "CAL"
            result = evaluate_expression(expression)  # Evaluate the expression
            print("Calculator:", result)  # Print the result
        else:
            # Get the response based on user input
            response = get_response(user_input)
            if response:
                print("Chatbot:", response)
            else:
                print("Chatbot: I'm sorry, I don't understand.")
                print("Chatbot: Can you teach me? What should I respond to that?")
                new_response = input("You: ")
                print("Chatbot: Got it, I'll remember that.")
                
                # Record user input and response to data
                data['qa_pairs'].append({
                    'question': user_input,
                    'answer': new_response
                })
                
                # Update corpus and re-fit CountVectorizer
                corpus.append(user_input)
                responses.append(new_response)
                X = vectorizer.fit_transform(corpus)
                    
                # Save updated data to file
                with open(data_file, 'w') as file:
                    json.dump(data, file, indent=4)
