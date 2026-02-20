"""
Unit tests for Todo and TodoList classes.
"""
import pytest
from src.models.todo import Todo, TodoList, Priority


class TestTodo:
    """Unit tests for the Todo class."""

    def test_todo_creation(self):
        """Test creating a Todo object with valid parameters."""
        todo = Todo(1, "Test title", "medium", False)
        assert todo.id == 1
        assert todo.title == "Test title"
        assert todo.priority == "medium"
        assert not todo.completed

    def test_todo_default_values(self):
        """Test creating a Todo object with default values."""
        todo = Todo(1, "Test title")
        assert todo.id == 1
        assert todo.title == "Test title"
        assert todo.priority == "medium"
        assert not todo.completed

    def test_todo_mark_completed(self):
        """Test marking a Todo as completed."""
        todo = Todo(1, "Test title")
        assert not todo.completed
        todo.mark_completed()
        assert todo.completed

    def test_todo_to_dict(self):
        """Test converting a Todo object to dictionary."""
        todo = Todo(1, "Test title", "high", True)
        expected_dict = {
            "id": 1,
            "title": "Test title",
            "priority": "high",
            "completed": True
        }
        assert todo.to_dict() == expected_dict

    def test_validate_priority_valid(self):
        """Test validating valid priority values."""
        todo = Todo(1, "Test title", "high")
        assert todo.priority == "high"

        todo = Todo(1, "Test title", "HIGH")  # Should normalize to lowercase
        assert todo.priority == "high"

        todo = Todo(1, "Test title", "LOW")  # Should normalize to lowercase
        assert todo.priority == "low"

    def test_validate_priority_invalid(self):
        """Test validating invalid priority values raises ValueError."""
        with pytest.raises(ValueError):
            Todo(1, "Test title", "invalid_priority")


class TestTodoList:
    """Unit tests for the TodoList class."""

    def test_todo_list_initialization(self):
        """Test initializing an empty TodoList."""
        todo_list = TodoList()
        assert len(todo_list.list_todos()) == 0
        assert todo_list.next_id == 1

    def test_add_todo_basic(self):
        """Test adding a basic todo to the list."""
        todo_list = TodoList()
        todo = todo_list.add("Test title")

        assert len(todo_list.list_todos()) == 1
        assert todo.id == 1
        assert todo.title == "Test title"
        assert todo.priority == "medium"
        assert not todo.completed

    def test_add_todo_with_priority(self):
        """Test adding a todo with a specific priority."""
        todo_list = TodoList()
        todo = todo_list.add("Test title", "high")

        assert len(todo_list.list_todos()) == 1
        assert todo.id == 1
        assert todo.title == "Test title"
        assert todo.priority == "high"
        assert not todo.completed

    def test_add_multiple_todos(self):
        """Test adding multiple todos and checking ID increment."""
        todo_list = TodoList()
        todo1 = todo_list.add("First todo")
        todo2 = todo_list.add("Second todo", "high")

        assert len(todo_list.list_todos()) == 2
        assert todo1.id == 1
        assert todo2.id == 2

        # Check the next_id is incremented correctly
        assert todo_list.next_id == 3

    def test_add_empty_title_raises_error(self):
        """Test that adding a todo with empty title raises ValueError."""
        todo_list = TodoList()

        with pytest.raises(ValueError):
            todo_list.add("")

        with pytest.raises(ValueError):
            todo_list.add("   ")  # Only whitespace

    def test_add_invalid_priority_raises_error(self):
        """Test that adding a todo with invalid priority raises ValueError."""
        todo_list = TodoList()

        with pytest.raises(ValueError):
            todo_list.add("Test title", "invalid_priority")

    def test_list_todos_preserves_order(self):
        """Test that list_todos preserves insertion order."""
        todo_list = TodoList()
        todo1 = todo_list.add("First")
        todo2 = todo_list.add("Second")
        todo3 = todo_list.add("Third")

        todos = todo_list.list_todos()
        assert len(todos) == 3
        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3

    def test_complete_existing_todo(self):
        """Test completing an existing todo."""
        todo_list = TodoList()
        todo = todo_list.add("Test todo")

        # Initially not completed
        assert not todo.completed

        # Complete the todo
        result = todo_list.complete(1)
        assert result is True  # Operation succeeded

        # Check that the todo is now completed
        assert todo.completed

    def test_complete_nonexistent_todo(self):
        """Test completing a non-existent todo returns False."""
        todo_list = TodoList()
        result = todo_list.complete(999)
        assert result is False

    def test_show_existing_todo(self):
        """Test showing an existing todo."""
        todo_list = TodoList()
        added_todo = todo_list.add("Test todo")

        retrieved_todo = todo_list.show(1)
        assert retrieved_todo is not None
        assert retrieved_todo.id == added_todo.id
        assert retrieved_todo.title == added_todo.title

    def test_show_nonexistent_todo(self):
        """Test showing a non-existent todo returns None."""
        todo_list = TodoList()
        retrieved_todo = todo_list.show(999)
        assert retrieved_todo is None

    def test_get_todo_by_id_existing(self):
        """Test getting an existing todo by ID."""
        todo_list = TodoList()
        added_todo = todo_list.add("Test todo")

        retrieved_todo = todo_list.get_todo_by_id(1)
        assert retrieved_todo is not None
        assert retrieved_todo.id == added_todo.id
        assert retrieved_todo.title == added_todo.title

    def test_get_todo_by_id_nonexistent(self):
        """Test getting a non-existent todo by ID returns None."""
        todo_list = TodoList()
        retrieved_todo = todo_list.get_todo_by_id(999)
        assert retrieved_todo is None