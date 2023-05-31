from flask import Flask, jsonify, request
import re


# Path to your SGF file
sgf_file_path = "./sgf/example-game.sgf"

# Parse SGF File
with open(sgf_file_path, 'r', encoding='utf-8') as file:
    sgf_content = file.read()

# Extract the moves using regular expressions
move_regex = re.compile(r";[BW]\[[a-z]{0,2}\]")
moves = move_regex.findall(sgf_content)

# Clean up the moves and remove unnecessary characters
clean_moves = [move.strip(";").replace("B[", "").replace("W[", "").replace("]","") for move in moves]

# Print the extracted moves
for move in clean_moves:
    print(move)

# def translate_letter_to_cx_number(letter):
#     alphabet = 'abcdefghijklmnopqrstuvwxyz'
#     number = alphabet.index(letter) * 5 + 3
#     return number

# # Test the translation
# letters = ['a', 'b', 'c', 't']
# numbers = [translate_letter_to_number(letter) for letter in letters]
# print(numbers)  # Output: [3, 8, 13, 93]















app = Flask(__name__)

# Sample data
tasks = [
    {"id": 1, "title": "Task 1", "completed": False},
    {"id": 2, "title": "Task 2", "completed": True},
]

# Endpoint to get all tasks


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Endpoint to get a specific task


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify(task)
    else:
        return jsonify({"message": "Task not found"}), 404

# Endpoint to create a new task


@app.route('/api/tasks', methods=['POST'])
def create_task():
    task = {
        "id": len(tasks) + 1,
        "title": request.json.get('title'),
        "completed": False
    }
    tasks.append(task)
    return jsonify(task), 201

# Endpoint to update an existing task


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        task['title'] = request.json.get('title', task['title'])
        task['completed'] = request.json.get('completed', task['completed'])
        return jsonify(task)
    else:
        return jsonify({"message": "Task not found"}), 404

# Endpoint to delete a task


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"message": "Task deleted"})


if __name__ == '__main__':
    app.run(debug=True)
