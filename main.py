class ToDoList:

    def __init__(self):
        self.tasks = []

    # Просмотр всех задач
    def show_tasks(self):
        # Проверка на наличие задач
        if not self.tasks:
            print("\nУ вас еще нет задач")
            return

        # Вывод задач, если они уже есть
        print("\nСписок задач:")
        for i in range(len(self.tasks)):
            print(f'{i + 1}. {self.tasks[i]["name"]} - {self.tasks[i]["status"]}')

    # Добавление задачи
    def add_task(self):
        while True:
            task = input("\nВведите свою задачу (или 0 для возврата к меню): ").strip()

            # Проверка на ввод пустой строки
            if task == "":
                print("Ошибка: задача не может быть пустой.")
                continue

            # Проверка на возврат к меню
            if task == "0":
                return

            # Если условия выше не сработали, то создается словарь с задачей и добавляется в список
            new_task = {"name": task, "status": "Не выполнена"}
            self.tasks.append(new_task)
            print(f'\nЗадача "{new_task["name"]}" успешно добавлена!')
            return

    # Удаление задачи
    def delete_task(self):
        if not self.tasks:
            print("\nУ вас еще нет задач")
            return

        self.show_tasks()

        while True:
            choice = input(
                "\nВведите номер задачи для удаления (или 0 для возврата к меню): "
            ).strip()

            # Проверка на ввод именно номера задачи
            if not choice.isdigit():
                print("Введите номер задачи из вашего списка")
                continue

            # Меняем тип в одном месте, если только цифры введены
            choice = int(choice)

            # Проверка на выход в меню
            if choice == 0:
                return

            # Проверка на принадлежность введенного номера задачи к списку
            elif 1 <= choice <= len(self.tasks):
                deleted_task = self.tasks.pop(choice - 1)
                print(f'\nЗадача "{deleted_task["name"]}" удалена!')
                return
            else:
                print("У вас нет задачи под таким номером")
                continue

    # Изменение статуса задачи
    def mark_task(self):
        if not self.tasks:
            print("\nУ вас еще нет задач")
            return

        self.show_tasks()

        while True:
            choice = input(
                "\nВведите номер задачи для изменения статуса (или 0 для возврата к меню): "
            ).strip()

            # Проверка на ввод именно номера задачи
            if not choice.isdigit():
                print("Введите номер задачи из вашего списка")
                continue

            choice = int(choice)
            # Проверка на выход к меню
            if choice == 0:
                return

            # Проверка на принадлежность введенного номера задачи к списку
            elif 1 <= choice <= len(self.tasks):
                task = self.tasks[choice - 1]
                while True:
                    answer = (
                        input(
                            "\nВыполнили ли вы эту задачу? (да/нет или 0 для возврата к меню без изменения статуса) "
                        )
                        .strip()
                        .lower()
                    )

                    # Проверка на выход к меню
                    if answer == "0":
                        return

                    # Изменение статуса на выполненный
                    elif answer == "да":
                        task["status"] = "Выполнена"
                        print(f'\nЗадача "{task["name"]}" отмечена как выполненная!')
                        return

                    # Изменение статуса на невыполненный
                    elif answer == "нет":
                        task["status"] = "Не выполнена"
                        print(f'\nЗадача "{task["name"]}" отмечена как невыполненная!')
                        return

                    # Если ввели посторонний текст
                    else:
                        print('\nВведите "да" или "нет".')
                        continue

            else:
                print("У вас нет задачи под таким номером")
                continue

    # Просмотр статистики
    def show_statistics(self):
        # Проверка на наличие задач
        if not self.tasks:
            print("У вас еще нет задач")
            return

        total = len(self.tasks)
        not_completed = 0
        completed = 0

        # Подсчитываю количество выполненных/невыполненных задач
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
    {"num": 2, "text": "Добавить задачу в список", "action": todo.add_task},
    {"num": 3, "text": "Изменить статус задачи", "action": todo.mark_task},
    {"num": 4, "text": "Удалить задачу из списка", "action": todo.delete_task},
    {
        "num": 5,
        "text": "Посмотреть статистику по выполненным задачам",
        "action": todo.show_statistics,
    },
    {"num": 0, "text": "Завершить программу"},
]


def show_menu():
    print("\nМеню задач:")

    # Вывод списка меню
    for i in menu:
        print(f'{i["num"]}. {i["text"]}')

    choice = input("Введите номер пункта меню: ").strip()

    if choice == "0":
        print("Программа завершена.")
        return False

    # Вызывается соответствующий метод по введенному номеру пункта меню
    for i in menu:
        if str(i["num"]) == choice:
            i["action"]()
            return True

    print("\nТакого пункта меню нет, введите номер еще раз.")
    return True


print("===== Добро пожаловать в список ваших задач =====")

# Вызывается меню до тех пор, пока не введем 0
if __name__ == "__main__":
    while True:
        if not show_menu():
            break
