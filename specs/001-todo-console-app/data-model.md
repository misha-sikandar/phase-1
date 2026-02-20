# Data Model: Todo Evolution Console Application

## Todo Entity

**Definition**: Represents a single todo item with associated properties

**Attributes**:
- `id` (int): Unique incremental identifier assigned when the todo is created
- `title` (str): The text description of the todo item
- `priority` (str): Priority level of the todo (values: "low", "medium", "high")
- `completed` (bool): Status indicating if the todo has been completed

**State Transitions**:
- Initially: `completed = False`
- After `complete <id>` command: `completed = True`

**Validation Rules**:
- `id` must be unique and assigned incrementally
- `title` must be a non-empty string
- `priority` must be one of: "low", "medium", "high" (defaults to "medium")
- `completed` is boolean (defaults to False)

## TodoList Entity

**Definition**: Collection of Todo items that preserves insertion order and supports operations

**Attributes**:
- `todos` (list): Ordered collection of Todo objects
- `next_id` (int): Counter for assigning the next unique ID

**Operations**:
- `add(title, priority="medium")`: Creates a new Todo with unique ID and adds to the list
- `list()`: Returns all todos preserving insertion order
- `complete(id)`: Marks a todo as completed by ID
- `show(id)`: Returns details of a specific todo by ID

**Validation Rules**:
- Must preserve insertion order of todos
- IDs must be unique and incrementally assigned
- Operations must validate existence of referenced todos
- Priority values must be validated before creating todos

## Relationships

- TodoList contains zero or more Todo entities
- Each Todo belongs to exactly one TodoList instance
- TodoList manages the lifecycle of contained Todo entities