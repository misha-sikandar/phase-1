"""
Module containing the Todo and TodoList classes for the console application.
"""

from typing import List, Optional
from enum import Enum


class Priority(Enum):
    """Enumeration for todo priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo:
    """Represents a single todo item with associated properties."""

    def __init__(self, id: int, title: str, priority: str = "medium", completed: bool = False):
        """
        Initialize a Todo object.

        Args:
            id: Unique incremental identifier assigned when the todo is created
            title: The text description of the todo item
            priority: Priority level of the todo (values: "low", "medium", "high")
            completed: Status indicating if the todo has been completed
        """
        self.id = id
        self.title = title
        self.priority = self._validate_priority(priority)
        self.completed = completed

    def _validate_priority(self, priority: str) -> str:
        """
        Validate the priority value and return the validated priority.

        Args:
            priority: Priority level to validate

        Returns:
            Validated priority level

        Raises:
            ValueError: If the priority is not one of the allowed values
        """
        if priority.lower() not in [p.value for p in Priority]:
            raise ValueError(f"Priority must be one of: {[p.value for p in Priority]}")
        return priority.lower()

    def mark_completed(self):
        """Mark the todo as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """
        Convert the Todo object to a dictionary representation.

        Returns:
            Dictionary representation of the Todo object
        """
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed
        }


class TodoList:
    """Collection of Todo items that preserves insertion order and supports operations."""

    def __init__(self):
        """Initialize an empty TodoList with a counter for unique IDs."""
        self.todos: List[Todo] = []
        self.next_id = 1

    def add(self, title: str, priority: str = "medium") -> Todo:
        """
        Create a new Todo with unique ID and add to the list.

        Args:
            title: The title of the new todo
            priority: The priority level of the new todo (default: "medium")

        Returns:
            The newly created Todo object

        Raises:
            ValueError: If title is empty or priority is invalid
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        # Validate priority before creating the todo
        priority_enum = Priority(priority.lower())

        todo = Todo(self.next_id, title.strip(), priority.lower())
        self.todos.append(todo)
        self.next_id += 1
        return todo

    def list_todos(self) -> List[Todo]:
        """
        Return all todos preserving insertion order.

        Returns:
            List of all Todo objects in insertion order
        """
        return self.todos.copy()

    def complete(self, id: int) -> bool:
        """
        Mark a todo as completed by ID.

        Args:
            id: The ID of the todo to mark as completed

        Returns:
            True if the todo was found and marked as completed, False otherwise
        """
        for todo in self.todos:
            if todo.id == id:
                todo.mark_completed()
                return True
        return False

    def show(self, id: int) -> Optional[Todo]:
        """
        Return details of a specific todo by ID.

        Args:
            id: The ID of the todo to retrieve

        Returns:
            The Todo object if found, None otherwise
        """
        for todo in self.todos:
            if todo.id == id:
                return todo
        return None

    def get_todo_by_id(self, id: int) -> Optional[Todo]:
        """
        Get a todo by its ID.

        Args:
            id: The ID of the todo to retrieve

        Returns:
            The Todo object if found, None otherwise
        """
        for todo in self.todos:
            if todo.id == id:
                return todo
        return None