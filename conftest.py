import pytest
from main import ToDoList

@pytest.fixture
def empty_todo():
    """Пустой список задач."""
    return ToDoList()

@pytest.fixture
def todo_with_tasks():
    """Список с двумя задачами."""
    todo = ToDoList()
    todo.tasks = [
        {"name": "Прогуляться", "status": "Не выполнена"},
        {"name": "Поспать", "status": "Выполнена"},
    ]
    return todo