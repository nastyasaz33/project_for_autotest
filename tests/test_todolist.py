import pytest

class TestAddTask:
    #Успешное добавление задачи
    def test_add_task(self, empty_todo, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "Прогуляться")
        empty_todo.add_task()

        assert len(empty_todo.tasks) == 1, "Задача не была добавлена"
        assert empty_todo.tasks[0]["name"] == "Прогуляться", "Задача добавилась с некорректным названием"
        assert empty_todo.tasks[0]["status"] == "Не выполнена", "Задача добавилась с уже выполненным статусом"

# Проверка, что добавится только одна задача без пустой 
    def test_add_empty_task(self, empty_todo, monkeypatch):
        inputs_tasks = ["", "Прогуляться"]
        monkeypatch.setattr("builtins.input", lambda _: inputs_tasks.pop(0))
        empty_todo.add_task()
    
        assert len(empty_todo.tasks) == 1, "Была добавлена лишняя задача или не добавлена ни одна задача"
        assert empty_todo.tasks[0]["name"] == "Прогуляться", "Задача добавилась с некорректным названием"
        assert empty_todo.tasks[0]["status"] == "Не выполнена", "Задача добавилась с уже выполненным статусом"


class TestDelete:
    #Успешное удаление задачи из списка
    def test_delete_task(self, todo_with_tasks, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "1")
        todo_with_tasks.delete_task()

        assert len(todo_with_tasks.tasks) == 1, "Задача не удалилась или была удалена лишняя задача"
        assert todo_with_tasks.tasks[0]["name"] == "Поспать", "Удалилась другая задача"

    #Валидация на удаление задачи из списка
    @pytest.mark.parametrize("task_number", ["qwe", "12", "-1"])
    def test_delete_different_tasks(self, todo_with_tasks, monkeypatch, task_number):
        inputs_number_task = [task_number, "0"]
        monkeypatch.setattr("builtins.input", lambda _: inputs_number_task.pop(0))
        todo_with_tasks.delete_task()

        assert len(todo_with_tasks.tasks) == 2, "Была удалена неподходящая задача"


class TestChangeStatus:
    #Валидация на изменение статуса задачи
    @pytest.mark.parametrize("task_number, changed_status, task_status", [("1", "да", "Выполнена"), ( "2","нет", "Не выполнена")])
    def test_change_status(self, todo_with_tasks, monkeypatch, task_number, changed_status, task_status):
        inputs_change_task = [task_number, changed_status]
        monkeypatch.setattr("builtins.input", lambda _: inputs_change_task.pop(0))
        todo_with_tasks.mark_task()

        assert todo_with_tasks.tasks[int(task_number) - 1]["status"] == task_status, f'Статус задачи изменён некорректно. Ожидалось: {task_status}'

    #Проверка на некорректные данные для изменения статуса задачи      
    @pytest.mark.parametrize("task_number", ["qwe", "12", "-1"])
    def test_invalid_change_status(self, todo_with_tasks, monkeypatch, task_number):
        inputs_number_task = [task_number, "0"]
        monkeypatch.setattr("builtins.input", lambda _: inputs_number_task.pop(0))
        todo_with_tasks.mark_task()
        

        assert todo_with_tasks.tasks[0]["status"] == "Не выполнена", "Статус задачи не должен был измениться"
        assert todo_with_tasks.tasks[1]["status"] == "Выполнена", "Статус задачи не должен был измениться"

    def test_back_to_menu_without_changing_status(self, todo_with_tasks, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "0")
        todo_with_tasks.mark_task()

        assert (
            todo_with_tasks.tasks[0] == {"name": "Прогуляться", "status": "Не выполнена"}
            and
            todo_with_tasks.tasks[1] == {"name": "Поспать", "status": "Выполнена"}
        ), "Статус задач изменился, хотя пользователь выбрал возврат в меню"

class TestTaskStatistics:
    #Проверка статистики по задачам
    def test_statistics(self, todo_with_tasks):

        assert todo_with_tasks.show_statistics() == (2, 1, 1), "Статистика вычисляется некорректно"
        