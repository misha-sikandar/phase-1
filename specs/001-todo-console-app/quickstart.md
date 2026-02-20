# Quickstart Guide: Todo Evolution Console Application

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## Installation

1. Clone or download the repository
2. Navigate to the project directory
3. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```
   (Note: For Phase 1, there are no external dependencies beyond Python standard library)

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