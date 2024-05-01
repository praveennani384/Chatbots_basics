# Chatbots_basics
types of chatbots sql_query_generator, calculator, and general_chatbot with adaptive learning capability

#SQL usage

To initiate SQL operations, type "SQL" or "sql" and then choose the action you want to perform: create, insert, update, delete, select, or describe.

For creating a table, select "create" and enter the table name followed by the column names and types.

For inserting data into a table, choose "insert" and provide the table name and column values.

For updating existing records, select "update" and specify the table name, column to update, new value, and condition.

For deleting records, choose "delete" and enter the table name along with the condition.

To retrieve data from a table, select "select" and provide the table name, columns to select, conditions, and ordering if needed.

To describe the structure of a table, select "describe" and enter the table name.

Follow the prompts for each action to complete the SQL operation.

#CALCULATOR usage

1. To initiate the calculator feature, type "CAL" or "cal" followed by the expression you want to evaluate.
2. Use the following operators for arithmetic operations: + (addition), - (subtraction), * (multiplication), / (division), ** (exponentiation).
3. For example, type "CAL 10 + 5" to perform addition and get the result.
4. The calculator also handles general chat interactions. Simply type your message, and the chatbot will respond based on previous interactions.
5. If the chatbot doesn't understand your message, it will ask you to teach it. Provide a response, and the chatbot will remember it for future interactions.
6. You can exit the program by typing "exit".

#GENERAL CHATBOT

1. Start the chatbot by running the code.
2. You can interact with the chatbot by typing your message after the prompt "You: ".
3. If the chatbot doesn't understand your query or you want to teach it a new question-answer pair:

    3.1 Type "change: your_question_here" to change or add a new question-answer pair.

    3.2 If the chatbot suggests a similar question, respond with "yes" or "no":

        3.2.1 If "yes", provide the correct answer to the suggested question.

        3.2.2 If "no", enter the correct question along with its answer.
5. The chatbot learns from your interactions and saves the new question-answer pairs to a file for future reference.
6. To exit the chatbot, type "exit".
