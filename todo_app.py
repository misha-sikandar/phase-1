#!/usr/bin/env python3
"""
Main application entry point for the Todo Evolution Console Application.
"""
import sys
from src.models.todo import TodoList
from src.cli.main import create_parser, handle_command


def main():
    """
    Main function to run the Todo Evolution Console Application.
    """
    # Initialize TodoList instance
    todo_list = TodoList()

    # Create argument parser
    parser = create_parser()

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse command line arguments
    args = parser.parse_args()

    # Handle the command
    result = handle_command(todo_list, args)

    # Print the result
    print(result)


if __name__ == "__main__":
    main()