#!/usr/bin/env python3
"""
Interactive Todo Console Application for the Todo Evolution Console Application.
"""
import sys
from src.models.todo import TodoList


def display_menu():
    """Display the menu options to the user."""
    print("\n" + "="*50)
    print("TODO EVOLUTION CONSOLE APPLICATION")
    print("="*50)
    print("1. Add Todo")
    print("2. List All Todos")
    print("3. Complete Todo")
    print("4. Show Todo Details")
    print("5. Exit")
    print("-"*50)


def get_user_choice():
    """Get and validate user's menu choice."""
    try:
        choice = input("Enter your choice (1-5): ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
            return None
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)


def handle_add_todo(todo_list):
    """Handle adding a new todo."""
    try:
        title = input("Enter todo title: ").strip()
        if not title:
            print("Title cannot be empty!")
            return

        print("Choose priority:")
        print("1. Low")
        print("2. Medium (default)")
        print("3. High")

        priority_choice = input("Enter priority (1-3, default is 2): ").strip()
        priority_map = {'1': 'low', '2': 'medium', '3': 'high'}

        if priority_choice in priority_map:
            priority = priority_map[priority_choice]
        else:
            priority = 'medium'  # default

        new_todo = todo_list.add(title, priority)
        print(f"\n✓ Added todo with ID {new_todo.id}: '{new_todo.title}' (priority: {new_todo.priority})")
    except ValueError as e:
        print(f"✗ Error: {str(e)}")
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}")


def handle_list_todos(todo_list):
    """Handle listing all todos."""
    todos = todo_list.list_todos()

    if not todos:
        print("\nNo todos in the list.")
        return

    print("\n" + "-"*70)
    print(f"{'ID':<4} {'Title':<30} {'Priority':<10} {'Completed':<10}")
    print("-"*70)

    for todo in todos:
        status = "✓" if todo.completed else " "
        print(f"{todo.id:<4} {todo.title[:28]:<30} {todo.priority:<10} [{status}]")

    print("-"*70)


def handle_complete_todo(todo_list):
    """Handle completing a todo."""
    try:
        if not todo_list.list_todos():
            print("\nNo todos in the list to complete.")
            return

        todo_id = int(input("Enter the ID of the todo to complete: "))
        success = todo_list.complete(todo_id)

        if success:
            print(f"\n✓ Todo with ID {todo_id} marked as completed.")
        else:
            print(f"\n✗ Error: Todo with ID {todo_id} not found.")
    except ValueError:
        print("\n✗ Error: Please enter a valid ID number.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")


def handle_show_todo(todo_list):
    """Handle showing details of a specific todo."""
    try:
        if not todo_list.list_todos():
            print("\nNo todos in the list to show.")
            return

        todo_id = int(input("Enter the ID of the todo to show: "))
        todo = todo_list.show(todo_id)

        if todo:
            status = "Completed" if todo.completed else "Not Completed"
            print(f"\n{'='*30}")
            print(f"ID: {todo.id}")
            print(f"Title: {todo.title}")
            print(f"Priority: {todo.priority}")
            print(f"Status: {status}")
            print("="*30)
        else:
            print(f"\n✗ Error: Todo with ID {todo_id} not found.")
    except ValueError:
        print("\n✗ Error: Please enter a valid ID number.")
    except Exception as e:
        print(f"\n✗ Unexpected error: {str(e)}")


def main():
    """
    Main function to run the interactive Todo Evolution Console Application.
    """
    print("Welcome to Todo Evolution Console Application!")
    print("This is Phase 1 - In-memory console application.")

    # Initialize TodoList instance
    todo_list = TodoList()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice is None:
            continue  # Invalid input, show menu again

        if choice == '1':
            handle_add_todo(todo_list)
        elif choice == '2':
            handle_list_todos(todo_list)
        elif choice == '3':
            handle_complete_todo(todo_list)
        elif choice == '4':
            handle_show_todo(todo_list)
        elif choice == '5':
            print("\nThank you for using Todo Evolution Console Application!")
            print("Goodbye! 👋")
            break


if __name__ == "__main__":
    main()