import pytest

class TestAddTask:
    #Успешное добавление задачи
    def test_add_task(self, empty_todo, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "Прогуляться")
        empty_todo.add_task()

        assert len(empty_todo.tasks) == 1, "Задача не была добавлена"
        assert empty_todo.tasks[0]["name"] == "Прогуляться", "Задача добавилась с некорректным названием"
        assert empty_todo.tasks[0]["status"] == "Не выполнена", "Задача добавилась с уже выполненным статусом"

# Проверка, что добавится только одна задача без пустой строки
    def test_add_empty_task(self, empty_todo, monkeypatch):
        inputs_tasks = ["", "   ", "Прогуляться"]
        monkeypatch.setattr("builtins.input", lambda _: inputs_tasks.pop(0))
        empty_todo.add_task()
    
        assert len(empty_todo.tasks) == 1, "Была добавлена лишняя задача или не добавлена ни одна задача"
        assert empty_todo.tasks[0]["name"] == "Прогуляться", "Задача добавилась с некорректным названием"
        assert empty_todo.tasks[0]["status"] == "Не выполнена", "Задача добавилась с уже выполненным статусом"

    #Проверка на возврат к меню без добавления задачи к списку
    def test_add_task_empty_todo_list(self, empty_todo, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "0")

        assert empty_todo.add_task() == False, "Возврат к меню без добавления задачи не выполняется"


class TestDelete:
    #Успешное удаление задачи из списка
    def test_delete_task(self, todo_with_tasks, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "1")
        todo_with_tasks.delete_task()

        assert len(todo_with_tasks.tasks) == 1, "Задача не удалилась или была удалена лишняя задача"
        assert todo_with_tasks.tasks[0]["name"] == "Поспать", "Удалилась другая задача"

    #Валидация на удаление задачи из списка
    @pytest.mark.parametrize("task_number", ["qwe", "12", "-1"])
    def test_delete_invalid_task_number(self, todo_with_tasks, monkeypatch, task_number):
        inputs_number_task = [task_number, "0"]
        monkeypatch.setattr("builtins.input", lambda _: inputs_number_task.pop(0))
        todo_with_tasks.delete_task()

        assert len(todo_with_tasks.tasks) == 2, "Была удалена неподходящая задача"

    #Проверка на возврат в меню без удаления задачи
    def test_back_to_menu_without_delete_task(self, todo_with_tasks, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "0")
        todo_with_tasks.delete_task()
    
        assert len(todo_with_tasks.tasks) == 2,"Была удалена задача вместо возврата к меню"

    #Проверка на удаление задачи в пустом списке
    def test_delete_task_empty_todo_list(self, empty_todo):

        assert empty_todo.delete_task() == False, "Удаление задачи выполняется на пустом списке"


class TestChangeStatus:
    # Успешное изменение статуса задачи
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
        
        assert todo_with_tasks.tasks[0]["status"] == "Не выполнена", "Статус первой задачи изменился после некорректного ввода"
        assert todo_with_tasks.tasks[1]["status"] == "Выполнена", "Статус второй задачи изменился после некорректного ввода"

    #Проверка на возврат к меню
    def test_back_to_menu_from_change_status(self, todo_with_tasks, monkeypatch):
        monkeypatch.setattr("builtins.input", lambda _: "0")
        todo_with_tasks.mark_task()

        assert todo_with_tasks.tasks == [
            {"name": "Прогуляться", "status": "Не выполнена"},
            {"name": "Поспать", "status": "Выполнена"}
        ],"Статус задач изменился, хотя пользователь выбрал возврат в меню без изменения статуса"

    #Проверка на возврат к меню после выбора задачи, но без изменения ее статуса
    def test_back_to_menu_without_changing_status(self, todo_with_tasks, monkeypatch):
        input_task = ["1", "0"]
        monkeypatch.setattr("builtins.input", lambda _: input_task.pop(0))
        todo_with_tasks.mark_task()
    
        assert todo_with_tasks.tasks == [
            {"name": "Прогуляться", "status": "Не выполнена"},
            {"name": "Поспать", "status": "Выполнена"}
        ],"Статус задач изменился, хотя пользователь выбрал возврат в меню без изменения статуса"

    #Проверка на изменение статуса в пустом списке
    def test_change_status_empty_todo_list(self, empty_todo):

        assert empty_todo.mark_task() == False, "Изменение статуса выполняется на пустом списке"

class TestTaskStatistics:
    #Проверка статистики по списку с задачами
    def test_statistics(self, todo_with_tasks):

        total, completed, not_completed = todo_with_tasks.show_statistics()

        assert (total, completed, not_completed) == (2, 1, 1), (
            f"Ожидалось 2 задачи: 1 выполнена, 1 не выполнена.\n"
            f"Получено {total} задач: {completed} выполнено, {not_completed} не выполнено"
        )

    #Проверка статистики по пустому списку
    def test_statistics_empty_todo_list(self, empty_todo):

        assert empty_todo.show_statistics() == (0, 0, 0), "Статистика вычисляется некорректно при пустом списке"