# Todo Evolution Console Application

A simple console-based todo application that allows users to add, list, complete, and show todo items. This application follows Phase I constraints with in-memory storage only, single-process execution, and deterministic behavior.

## Features

- Add todo items with titles and optional priority levels
- List all todos with their details (ID, title, priority, completion status)
- Mark todos as completed
- Show detailed information about specific todos

## Usage

### Running the Application

```bash
python todo_app.py [command] [arguments]
```

### Available Commands

#### Add a Todo
```bash
python todo_app.py add "Buy groceries" --priority=high
```
- Creates a new todo with the specified title
- Optionally specify priority as low, medium, or high (defaults to medium)
- Returns the created todo's ID

#### List All Todos
```bash
python todo_app.py list
```
- Displays all todos with their ID, title, priority, and completion status
- Preserves insertion order

#### Complete a Todo
```bash
python todo_app.py complete 1
```
- Marks the todo with the specified ID as completed
- Replace `1` with the actual ID of the todo you want to complete

#### Show Todo Details
```bash
python todo_app.py show 1
```
- Displays detailed information about the todo with the specified ID
- Shows ID, title, priority, and completion status

### Examples

```bash
# Add a new todo with default priority (medium)
python todo_app.py add "Finish report"

# Add a new todo with high priority
python todo_app.py add "Call doctor" --priority=high

# List all todos
python todo_app.py list

# Complete a todo (assuming it has ID 1)
python todo_app.py complete 1

# Show details of a specific todo (assuming it has ID 1)
python todo_app.py show 1
```

## Development

This project uses Python 3.11 with no external dependencies beyond the Python standard library. All functionality is contained in memory during execution.

### Running Tests

```bash
pytest tests/
```

### Project Structure
- `src/models/todo.py`: Contains Todo and TodoList classes
- `src/cli/main.py`: Main CLI entry point
- `src/lib/constants.py`: Application constants
- `tests/unit/test_todo.py`: Unit tests for todo functionality
- `tests/integration/test_cli.py`: Integration tests for CLI
- `todo_app.py`: Main application entry point