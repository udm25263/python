from flask import Flask, request, jsonify

"""Initialize the Flask application"""
app = Flask(__name__)

"""In-memory dictionary to store tasks"""
tasks = {}

"""Counter to assign unique IDs to tasks"""
task_counter = 1

@app.route('/')
def home():
    """Home route to show welcome message"""
    return "Welcome to the Task Manager API! Use /tasks to manage tasks."

@app.route('/tasks', methods=['GET'])
def list_tasks():
    """Return all tasks as JSON"""
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    """Create a new task from client-provided JSON"""
    global task_counter
    data = request.get_json()

    """Validate input"""
    if not data or 'title' not in data:
        return jsonify({'error': 'Task title is required'}), 400

    """Generate new task ID and store the task"""
    task_id = task_counter
    tasks[task_id] = {
        'id': task_id,                # Unique identifier for the task
        'title': data['title'],       # Title of the task
        'completed': False            # Default completion status
    }
    task_counter += 1

    """Return the newly created task with status code 201 (Created)"""
    return jsonify(tasks[task_id]), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retrieve a task by ID"""
    task = tasks.get(task_id)
    if not task:
        """Return error if task not found"""
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update the title and/or completion status of an existing task"""
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    """Update fields if provided"""
    task['title'] = data.get('title', task['title'])
    task['completed'] = data.get('completed', task['completed'])

    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID"""
    if task_id in tasks:
        del tasks[task_id]
        return '', 204  # No content response for successful deletion
    return jsonify({'error': 'Task not found'}), 404

"""Entry point for running the application"""
if __name__ == '__main__':
    """Run the Flask development server"""
    app.run()
