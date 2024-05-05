import os
import datetime

# Класс Record с инициализацией основных параметров
class Record:
    def __init__(self, date, category, amount, description):
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

#Класс FinancialWallet с инициализацией пути файла
class FinancialWallet:
    def __init__(self, file_path):
        self.file_path = file_path

# Функция load_records() для инициализации файла с записями
    def load_records(self):
        records = []
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                lines = file.readlines()
                for i in range(0, len(lines), 5):
                    record = Record(
                        date=datetime.datetime.strptime(lines[i].strip('\n').split(': ')[1], '%Y-%m-%d'),
                        category=lines[i+1].strip('\n').split(': ')[1],
                        amount=float(lines[i+2].strip('\n').split(': ')[1]),
                        description=lines[i+3].strip('\n').split(': ')[1]
                    )
                    records.append(record)
        return records

# Функция save_records() для сохранения внесенных измеенений
    def save_records(self, records):
        with open(self.file_path, 'w') as file:
            for record in records:
                file.write(f"Дата: {record.date.strftime('%Y-%m-%d')}\n")
                file.write(f"Категория: {record.category}\n")
                file.write(f"Сумма: {record.amount}\n")
                file.write(f"Описание: {record.description}\n\n")

# Функция add_record() для добавления новых записей в файл с записями
    def add_record(self):
        date = input("Введите дату (гггг-мм-дд): ")
        category = input("Введите категорию (Доход/Расход): ")
        amount = float(input("Введите сумму: "))
        description = input("Введите описание: ")
        record = Record(datetime.datetime.strptime(date, '%Y-%m-%d'), category, amount, description)
        records = self.load_records()
        records.append(record)
        self.save_records(records)

# Функция edit_record() для изменения уже имеющихся записей в файле с записями
    def edit_record(self, index):
        records = self.load_records()
        if 0 <= index < len(records):
            print("Текущая запись:")
            print(f"Дата: {records[index].date.strftime('%Y-%m-%d')}")
            print(f"Категория: {records[index].category}")
            print(f"Сумма: {records[index].amount}")
            print(f"Описание: {records[index].description}")
            print()
            date = input("Введите новую дату (гггг-мм-дд): ")
            category = input("Введите новую категорию (Доход/Расход): ")
            amount = float(input("Введите новую сумму: "))
            description = input("Введите новое описание: ")
            records[index] = Record(datetime.datetime.strptime(date, '%Y-%m-%d'), category, amount, description)
            self.save_records(records)
        else:
            print("Ошибка: неверный индекс записи")

# Функция search_records() для поиска и вывода записи по ее параметрам
    def search_records(self, category=None, date=None, amount=None, description=None):
        records = self.load_records()
        results = []
        for record in records:
            if (record.category == category) and (record.amount == amount) and (record.description == description):
                results.append(record)
        return results

# Функция get_balance() для вывода баланса исходя из данных в файле с записисями
    def get_balance(self):
        records = self.load_records()
        income = sum(record.amount for record in records if record.category == 'Доход')
        expenses = sum(record.amount for record in records if record.category == 'Расход')
        balance = income - expenses
        return balance, income, expenses

if __name__ == "__main__":
    wallet = FinancialWallet("records.txt") # Создание объекта wallet класса FiniancialWallet

# Цикл для выбора действия программы
    while True:
        print("\nВыберите действие:")
        print("1. Вывести баланс")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Выйти")

        choice = input("Введите номер действия: ")

        if choice == "1":
            balance, income, expenses = wallet.get_balance()
            print(f"Текущий баланс: {balance}")
            print(f"Доходы: {income}")
            print(f"Расходы: {expenses}")
        elif choice == "2":
            wallet.add_record()
        elif choice == "3":
            index = int(input("Введите индекс записи для редактирования: "))
            wallet.edit_record(index)
        elif choice == "4":
            category = input("Введите категорию (Доход/Расход) или нажмите Enter для пропуска: ")
            date = input("Введите дату (гггг-мм-дд) или нажмите Enter для пропуска: ")
            amount = input("Введите сумму или нажмите Enter для пропуска: ")
            description = input("Введите описвание или нажммите Enter для пропуска: ")
            if amount:
                amount = float(amount)
            search_results = wallet.search_records(category=category, date=date, amount=amount, description=description)
            if search_results:
                print("\nНайденные записи:")
                for result in search_results:
                    print(f"Дата: {result.date.strftime('%Y-%m-%d')}, Категория: {result.category}, Сумма: {result.amount}, Описание: {result.description}")
            else:
                print("Записи не найдены.")
        elif choice == "5":
            break
        else:
            print("Ошибка: неверный выбор действия")
