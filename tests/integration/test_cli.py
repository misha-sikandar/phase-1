"""
Integration tests for the CLI functionality.
"""
import sys
from io import StringIO
from unittest.mock import patch
from src.cli.main import create_parser, handle_command
from src.models.todo import TodoList


class TestAddCommandIntegration:
    """Integration tests for the add command."""

    def test_add_command_with_default_priority(self):
        """Test adding a todo with default priority."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: add "Test todo"
        args = parser.parse_args(['add', 'Test', 'todo'])
        result = handle_command(todo_list, args)

        # Verify the result
        assert "Added todo with ID 1: 'Test todo' (priority: medium)" in result
        assert len(todo_list.list_todos()) == 1

        # Verify the todo was added correctly
        added_todo = todo_list.list_todos()[0]
        assert added_todo.id == 1
        assert added_todo.title == "Test todo"
        assert added_todo.priority == "medium"
        assert not added_todo.completed

    def test_add_command_with_high_priority(self):
        """Test adding a todo with high priority."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: add "Important task" --priority=high
        args = parser.parse_args(['add', 'Important', 'task', '--priority', 'high'])
        result = handle_command(todo_list, args)

        # Verify the result
        assert "Added todo with ID 1: 'Important task' (priority: high)" in result
        assert len(todo_list.list_todos()) == 1

        # Verify the todo was added correctly
        added_todo = todo_list.list_todos()[0]
        assert added_todo.id == 1
        assert added_todo.title == "Important task"
        assert added_todo.priority == "high"
        assert not added_todo.completed

    def test_add_command_with_low_priority(self):
        """Test adding a todo with low priority."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: add "Low priority task" --priority=low
        args = parser.parse_args(['add', 'Low', 'priority', 'task', '--priority', 'low'])
        result = handle_command(todo_list, args)

        # Verify the result
        assert "Added todo with ID 1: 'Low priority task' (priority: low)" in result
        assert len(todo_list.list_todos()) == 1

        # Verify the todo was added correctly
        added_todo = todo_list.list_todos()[0]
        assert added_todo.id == 1
        assert added_todo.title == "Low priority task"
        assert added_todo.priority == "low"
        assert not added_todo.completed

    def test_add_command_missing_title(self):
        """Test adding a todo without title shows error message."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: add (without title)
        # Note: This will likely fail at the argparser level, but let's test the handler
        try:
            args = parser.parse_args(['add'])
            result = handle_command(todo_list, args)
            # If we get here, the error handling should be in the result
            assert "Error" in result
        except SystemExit:
            # argparse exits when required arguments are missing
            pass

    def test_add_command_empty_title(self):
        """Test adding a todo with empty title shows error message."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: add "" (empty title)
        args = parser.parse_args(['add', ''])
        result = handle_command(todo_list, args)

        # Verify the error message
        assert "Error" in result
        assert "Title cannot be empty" in result
        assert len(todo_list.list_todos()) == 0

    def test_add_command_invalid_priority(self):
        """Test adding a todo with invalid priority shows error message."""
        todo_list = TodoList()
        parser = create_parser()

        # Note: argparse will catch invalid priority values, so we'll simulate directly
        # For this test, we'll test the internal validation
        try:
            # We'll create a mock args object to bypass argparse validation
            class MockArgs:
                command = 'add'
                title = ['Test todo']
                priority = 'invalid_priority'

            args = MockArgs()
            result = handle_command(todo_list, args)
            # This should trigger the ValueError in the Todo constructor
        except ValueError:
            # Expected behavior
            pass


class TestListCommandIntegration:
    """Integration tests for the list command."""

    def test_list_empty_todos(self):
        """Test listing when there are no todos."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: list
        args = parser.parse_args(['list'])
        result = handle_command(todo_list, args)

        # Verify the result
        assert "No todos in the list." in result

    def test_list_single_todo(self):
        """Test listing when there is one todo."""
        todo_list = TodoList()
        # Add a todo first
        todo_list.add("Test todo", "medium")

        parser = create_parser()

        # Simulate command line arguments: list
        args = parser.parse_args(['list'])
        result = handle_command(todo_list, args)

        # Verify the result contains the todo
        assert "Test todo" in result
        assert "medium" in result
        assert "1   Test todo" in result  # The ID and title should appear in the table

    def test_list_multiple_todos(self):
        """Test listing when there are multiple todos."""
        todo_list = TodoList()
        # Add multiple todos
        todo_list.add("First todo", "high")
        todo_list.add("Second todo", "medium")
        todo_list.add("Third todo", "low")

        parser = create_parser()

        # Simulate command line arguments: list
        args = parser.parse_args(['list'])
        result = handle_command(todo_list, args)

        # Verify the result contains all todos
        assert "First todo" in result
        assert "Second todo" in result
        assert "Third todo" in result
        assert "high" in result
        assert "medium" in result
        assert "low" in result
        assert result.count("   ") >= 3  # At least three todo entries in the table


class TestCompleteCommandIntegration:
    """Integration tests for the complete command."""

    def test_complete_existing_todo(self):
        """Test completing an existing todo."""
        todo_list = TodoList()
        # Add a todo first
        todo_list.add("Test todo", "medium")

        parser = create_parser()

        # Simulate command line arguments: complete 1
        args = parser.parse_args(['complete', '1'])
        result = handle_command(todo_list, args)

        # Verify the result
        assert "marked as completed" in result

        # Verify the todo is actually completed
        todo = todo_list.show(1)
        assert todo is not None
        assert todo.completed

    def test_complete_nonexistent_todo(self):
        """Test completing a nonexistent todo shows error message."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: complete 999 (doesn't exist)
        args = parser.parse_args(['complete', '999'])
        result = handle_command(todo_list, args)

        # Verify the error message
        assert "not found" in result.lower()


class TestShowCommandIntegration:
    """Integration tests for the show command."""

    def test_show_existing_todo(self):
        """Test showing an existing todo."""
        todo_list = TodoList()
        # Add a todo first
        todo_list.add("Test todo", "high")

        parser = create_parser()

        # Simulate command line arguments: show 1
        args = parser.parse_args(['show', '1'])
        result = handle_command(todo_list, args)

        # Verify the result contains todo details
        assert "ID: 1" in result
        assert "Title: Test todo" in result
        assert "Priority: high" in result
        assert "Status: Not Completed" in result

    def test_show_completed_todo(self):
        """Test showing a completed todo."""
        todo_list = TodoList()
        # Add and complete a todo
        todo_list.add("Test todo", "medium")
        todo_list.complete(1)

        parser = create_parser()

        # Simulate command line arguments: show 1
        args = parser.parse_args(['show', '1'])
        result = handle_command(todo_list, args)

        # Verify the result shows completed status
        assert "ID: 1" in result
        assert "Status: Completed" in result

    def test_show_nonexistent_todo(self):
        """Test showing a nonexistent todo shows error message."""
        todo_list = TodoList()
        parser = create_parser()

        # Simulate command line arguments: show 999 (doesn't exist)
        args = parser.parse_args(['show', '999'])
        result = handle_command(todo_list, args)

        # Verify the error message
        assert "not found" in result.lower()