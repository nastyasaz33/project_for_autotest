class ToDoList:

    def __init__(self):
        self.tasks = []

    # Просмотр всех задач
    def show_tasks(self):
        if not self.tasks:
            print("\nУ вас еще нет задач")
            return

        print("\nСписок задач:")
        for i in range(len(self.tasks)):
            print(f'{i + 1}. {self.tasks[i]["name"]} - {self.tasks[i]["status"]}')

    # Добавление задачи
    def add_task(self):
        while True:
            task = input("\nВведите свою задачу (или 0 для возврата к меню): ").strip()

            if task == "":
                print("Ошибка: задача не может быть пустой.")
                continue

            if task == "0":
                return

            new_task = {"name": task, "status": "Не выполнена"}
            self.tasks.append(new_task)
            print(f'\nЗадача "{new_task["name"]}" успешно добавлена!')
            return

    # Удаление задачи
    def del_task(self):
        if not self.tasks:
            print("\nУ вас еще нет задач")
            return

        print("\nВыберите номер задачи для удаления:")
        self.show_tasks()

        try:
            choice = int(input("\nВведите номер задачи для удаления: "))

            if 1 <= choice <= len(self.tasks):
                deleted_task = self.tasks.pop(choice - 1)
                print(f'\nЗадача "{deleted_task["name"]}" удалена!')
            else:
                print("\nЗадачи с таким номером нет!")

        except ValueError:
            print("\nОшибка: введите номер задачи числом!")

    # Изменение статуса задачи
    def mark_task(self):
        if not self.tasks:
            print("\nУ вас еще нет задач")
            return

        print("\nВыберите номер задачи для изменения статуса:")
        self.show_tasks()

        try:
            choice = int(input("\nВведите номер задачи: "))

            if 1 <= choice <= len(self.tasks):
                task = self.tasks[choice - 1]

                while True:
                    answer = (
                        input("\nВыполнили ли вы эту задачу? (да/нет) ").strip().lower()
                    )

                    if answer == "да":
                        task["status"] = "Выполнена"
                        print(f'\nЗадача "{task["name"]}" отмечена как выполненная!')
                        break

                    elif answer == "нет":
                        task["status"] = "Не выполнена"
                        print(f'\nЗадача "{task["name"]}" отмечена как невыполненная!')
                        break

                    else:
                        print('\nВведите "да" или "нет".')

            else:
                print("\nЗадачи с таким номером нет!")

        except ValueError:
            print("\nОшибка: введите номер задачи числом!")

    # Просмотр статистики
    def show_statistics(self):
        if not self.tasks:
            print("У вас еще нет задач!")
            return

        total = len(self.tasks)
        not_completed = 0
        completed = 0

        for i in self.tasks:
            if i["status"] == "Выполнена":
                completed += 1
            else:
                not_completed += 1

        print("\nСтатистика")
        print(f"Всего задач: {total}")
        print(f"Выполнено: {completed}")
        print(f"Осталось: {not_completed}")


todo = ToDoList()

menu = [
    {"num": 1, "text": "Показать все задачи", "action": todo.show_tasks},
    {"num": 2, "text": "Добавить задачу", "action": todo.add_task},
    {"num": 3, "text": "Изменить статус задачи", "action": todo.mark_task},
    {"num": 4, "text": "Удалить задачу", "action": todo.del_task},
    {"num": 5, "text": "Посмотреть статистику", "action": todo.show_statistics},
    {"num": 0, "text": "Завершить программу"},
]


def show_menu():
    print("\nМеню задач:")

    for i in menu:
        print(f'{i["num"]}. {i["text"]}')

    choice = input("Выберите пункт: ")

    if choice == "0":
        print("Программа завершена.")
        return False

    for i in menu:
        if str(i["num"]) == choice:
            i["action"]()
            return True

    print("\nТакого пункта меню нет, введите еще раз.")
    return True


while True:
    if not show_menu():
        break
