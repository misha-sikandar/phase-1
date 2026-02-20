"""
Main CLI module for the Todo Evolution Console Application.
"""
import argparse
from typing import Optional
from src.models.todo import TodoList


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog='todo_app',
        description='A console-based todo application',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new todo')
    add_parser.add_argument('title', nargs='*', help='Title of the todo item')
    add_parser.add_argument('--priority', choices=['low', 'medium', 'high'],
                           default='medium', help='Priority level (default: medium)')

    # List command
    list_parser = subparsers.add_parser('list', help='List all todos')

    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark a todo as completed')
    complete_parser.add_argument('id', type=int, help='ID of the todo to complete')

    # Show command
    show_parser = subparsers.add_parser('show', help='Show details of a specific todo')
    show_parser.add_argument('id', type=int, help='ID of the todo to show')

    return parser


def handle_add_command(todo_list: TodoList, args) -> str:
    """
    Handle the 'add' command to add a new todo.

    Args:
        todo_list: The TodoList instance to add the todo to
        args: The parsed command line arguments

    Returns:
        A string message with the result of the operation
    """
    if not args.title:
        return "Error: Title is required for the add command"

    title = ' '.join(args.title)

    try:
        new_todo = todo_list.add(title, args.priority)
        return f"Added todo with ID {new_todo.id}: '{new_todo.title}' (priority: {new_todo.priority})"
    except ValueError as e:
        return f"Error: {str(e)}"


def handle_list_command(todo_list: TodoList, args) -> str:
    """
    Handle the 'list' command to display all todos.

    Args:
        todo_list: The TodoList instance to list todos from
        args: The parsed command line arguments

    Returns:
        A string with the formatted list of todos
    """
    todos = todo_list.list_todos()

    if not todos:
        return "No todos in the list."

    result_lines = []
    result_lines.append("ID  Title                        Priority   Completed")
    result_lines.append("--- ---------------------------- -------- -----------")

    for todo in todos:
        status = "✓" if todo.completed else " "
        result_lines.append(f"{todo.id:<3} {todo.title:<28} {todo.priority:<8} [{status}]")

    return "\n".join(result_lines)


def handle_complete_command(todo_list: TodoList, args) -> str:
    """
    Handle the 'complete' command to mark a todo as completed.

    Args:
        todo_list: The TodoList instance to complete the todo in
        args: The parsed command line arguments

    Returns:
        A string message with the result of the operation
    """
    success = todo_list.complete(args.id)

    if success:
        return f"Todo with ID {args.id} marked as completed."
    else:
        return f"Error: Todo with ID {args.id} not found."


def handle_show_command(todo_list: TodoList, args) -> str:
    """
    Handle the 'show' command to display details of a specific todo.

    Args:
        todo_list: The TodoList instance to show the todo from
        args: The parsed command line arguments

    Returns:
        A string with the details of the specified todo
    """
    todo = todo_list.show(args.id)

    if todo:
        status = "Completed" if todo.completed else "Not Completed"
        return (
            f"ID: {todo.id}\n"
            f"Title: {todo.title}\n"
            f"Priority: {todo.priority}\n"
            f"Status: {status}"
        )
    else:
        return f"Error: Todo with ID {args.id} not found."


def handle_command(todo_list: TodoList, args) -> str:
    """
    Handle the appropriate command based on the parsed arguments.

    Args:
        todo_list: The TodoList instance to perform operations on
        args: The parsed command line arguments

    Returns:
        A string message with the result of the operation
    """
    if args.command == 'add':
        return handle_add_command(todo_list, args)
    elif args.command == 'list':
        return handle_list_command(todo_list, args)
    elif args.command == 'complete':
        return handle_complete_command(todo_list, args)
    elif args.command == 'show':
        return handle_show_command(todo_list, args)
    else:
        return "Error: Unknown command. Use --help for available commands."