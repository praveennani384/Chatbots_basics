import json
import difflib

data_file = "data.json"
sql_output_file = "sql_outputs.json"

def load_data(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        # If the data file doesn't exist, return an empty dictionary
        return {"qa_pairs": []}

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def save_sql_output(filename, output):
    with open(filename, "a") as file:
        file.write(f',\n{{"Query": "{output}"}}\n')

def learn_from_user(data, question, answer):
    data['qa_pairs'].append({"question": question, "answer": answer})
    save_data(data_file, data)

def get_closest_question(data, question):
    known_questions = [qa["question"] for qa in data["qa_pairs"]]
    closest_match = difflib.get_close_matches(question, known_questions, n=1, cutoff=0.6)
    if closest_match:
        return closest_match[0]
    else:
        return None

def generate_sql_query(action, table_name=None, columns=None, condition=None, order_by=None, limit=None):
    if action.lower() == 'select':
        if columns.lower() == 'all':
            query = f"SELECT * FROM {table_name}"
        else:
            query = f"SELECT {columns} FROM {table_name}"
            
        if condition:
            query += f" WHERE {condition}"
            
        if order_by:
            query += f" ORDER BY {order_by}"
            
        if limit:
            query += f" LIMIT {limit}"
            
        query += ";"
        return query
    
    elif action.lower() == 'describe':
        return f"DESCRIBE {table_name};"
    
    elif action.lower() == 'create':
        columns_str = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns])
        return f"CREATE TABLE {table_name} ({columns_str});"
    
    elif action.lower() == 'insert':
        columns_str = ', '.join(columns.keys())
        values_str = ', '.join([f"'{value}'" if isinstance(value, str) else str(value) for value in columns.values()])
        return f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
    
    elif action.lower() == 'update':
        set_values = ', '.join([f"{col_name} = '{col_value}'" if isinstance(col_value, str) else f"{col_name} = {col_value}" for col_name, col_value in columns.items()])
        return f"UPDATE {table_name} SET {set_values} WHERE {condition};"
    
    elif action.lower() == 'delete':
        return f"DELETE FROM {table_name} WHERE {condition};"
    
    else:
        return "Invalid action specified."

def solve_sql_question(sql_query, database):
    # Here you would execute the SQL query against the database
    # For this example, let's just return a dummy result
    return "Dummy result for SQL query: " + sql_query

def chat():
    data = load_data(data_file)
    
    while True:
        user_input = input("You: ")
        
        # Check if the user introduces themselves with their name
        if "my name is" in user_input:
            # Extract the name from the input
            name = user_input.split("my name is")[1].strip()
            print(f"Chatbot: Hello {name}, nice to meet you! I am Chatbot.")
        else:
            closest_question = get_closest_question(data, user_input)
            if closest_question:
                answer = next(qa["answer"] for qa in data["qa_pairs"] if qa["question"] == closest_question)
                print("Chatbot:", answer)
            elif "SQL" in user_input.lower() or "sql" in user_input.lower():
                # Example of handling SQL-related question
                action = input("Enter the SQL action (select/describe/create/insert/update/delete): ")
                if action.lower() == 'select':
                    table_name = input("Enter the table name: ")
                    columns = input("Enter the columns to select (or 'all' for all columns): ")
                    condition = input("Enter the condition (optional): ")
                    order_by = input("Enter the column to order by (optional): ")
                    limit = input("Enter the limit (optional): ")
                elif action.lower() == 'describe' or action.lower() == 'create':
                    table_name = input("Enter the table name: ")
                    columns = []
                    while True:
                        column = input("Enter column name and type (e.g., 'column_name data_type'), or type 'done' to finish: ")
                        if column.lower() == 'done':
                            break
                        column_name, column_type = column.split()
                        columns.append((column_name, column_type))
                    condition = None
                    order_by = None
                    limit = None
                elif action.lower() == 'insert':
                    table_name = input("Enter the table name: ")
                    columns = {}
                    while True:
                        column_name = input("Enter column name: ")
                        column_value = input("Enter column value: ")
                        columns[column_name] = column_value
                        cont = input("Do you want to add another column? (yes/no): ")
                        if cont.lower() != 'yes':
                            break
                    condition = None
                    order_by = None
                    limit = None
                elif action.lower() == 'update':
                    table_name = input("Enter the table name: ")
                    columns = {}
                    while True:
                        column_name = input("Enter column name: ")
                        column_value = input("Enter new column value: ")
                        columns[column_name] = column_value
                        cont = input("Do you want to update another column? (yes/no): ")
                        if cont.lower() != 'yes':
                            break
                    condition = input("Enter the condition for updating (e.g., 'column_name = value'): ")
                    order_by = None
                    limit = None
                elif action.lower() == 'delete':
                    table_name = input("Enter the table name: ")
                    condition = input("Enter the condition for deleting (e.g., 'column_name = value'): ")
                    columns = None
                    order_by = None
                    limit = None
                else:
                    print("Invalid action specified.")
                    continue
                
                sql_query = generate_sql_query(action, table_name=table_name, columns=columns, condition=condition, order_by=order_by, limit=limit)
                print("Generated SQL query:", sql_query)
                
                # Save the SQL query output
                save_sql_output(sql_output_file, sql_query)
            else:
                print("Chatbot: Sorry, I don't know the answer. Can you teach me?")
                new_answer = input("You: ")
                learn_from_user(data, user_input, new_answer)

if __name__ == "__main__":
    chat()
