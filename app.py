import json
from typing import List, Dict
from datetime import datetime


class Book:
    """
    Класс представляет книгу с уникальными свойствами, такими как название, автор, год издания и статус.
    """

    def __init__(self, title: str, author: str, year: int):
        # Уникальный идентификатор книги, будет назначен библиотекой.
        self.id = None
        self.title = title  # Название книги
        self.author = author  # Автор книги
        self.year = year  # Год издания книги
        self.status = "в наличии"  # Статус книги по умолчанию

    def to_dict(self) -> Dict:
        """
        Преобразует объект книги в словарь.
        Это необходимо для сохранения книги в формате JSON.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def validate_year(year: str) -> bool:
        """
        Проверяет, что год является числом и находится в диапазоне от 1000 до текущего года.
        """
        if not year.isdigit():  # Проверяем, состоит ли строка только из цифр
            return False
        year_int = int(year)
        return 1000 <= year_int <= datetime.now().year  # Проверяем диапазон от 1000 до текущего года

    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Проверяет, что имя или фамилия содержат только буквы и начинаются с заглавной.
        """
        return name.isalpha() and name.istitle()  # Проверяем, что состоит только из букв и начинается с заглавной буквы


class Library:
    """
    Класс для управления библиотекой книг.
    Отвечает за загрузку, сохранение, добавление, удаление и поиск книг.
    """

    def __init__(self, data_file: str = "library.json", error_log: str = "error_log.json"):
        self.books: List[Book] = []  # Список всех книг в библиотеке
        self.data_file = data_file  # Имя файла для хранения данных о книгах
        self.error_log = error_log  # Имя файла для логирования ошибок
        self.load_books()  # Загружаем книги при создании объекта

    def load_books(self):
        """
        Загружает книги из файла JSON.
        В случае ошибки, логирует ошибку в error_log.
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Читаем данные из файла
                for book_data in data:
                    # Для каждой книги создаем объект Book и добавляем его в список
                    book = Book(book_data["title"], book_data["author"], book_data["year"])
                    book.id = book_data["id"]
                    book.status = book_data["status"]
                    self.books.append(book)
        except FileNotFoundError:
            self.books = []  # Если файл не найден, инициализируем пустой список книг
        except json.JSONDecodeError as e:
            self.log_error(f"Ошибка загрузки JSON: {e}")  # Логируем ошибку в случае некорректного формата JSON
            self.books = []

    def save_books(self):
        """
        Сохраняет книги в файл JSON.
        В случае ошибки, логирует ошибку в error_log.
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                # Преобразуем книги в словари и сохраняем в файл
                json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)
        except Exception as e:
            self.log_error(f"Ошибка сохранения JSON: {e}")  # Логируем ошибку при сохранении данных

    def log_error(self, error_message: str):
        """
        Логирует ошибку в файл error_log.
        """
        try:
            with open(self.error_log, 'a', encoding='utf-8') as file:
                json.dump({"error": error_message}, file, ensure_ascii=False, indent=4)
        except Exception:
            pass  # Ошибка при логировании ошибки (не критично)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет новую книгу в библиотеку.
        Присваивает книге уникальный ID и сохраняет изменения.
        """
        book = Book(title, author, year)
        book.id = self.generate_id()  # Генерируем уникальный ID для книги
        self.books.append(book)
        self.save_books()  # Сохраняем изменения в файл

    def generate_id(self) -> int:
        """
        Генерирует уникальный идентификатор для книги.
        """
        return max((book.id for book in self.books),
                   default=0) + 1  # Генерация ID на основе максимального существующего

    def delete_book(self, book_id: int):
        """
        Удаляет книгу по ID.
        Если книга не найдена, вызывает ошибку.
        """
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)  # Удаляем книгу из списка
            self.save_books()  # Сохраняем изменения
        else:
            raise ValueError(f"Книга с ID {book_id} не найдена.")  # Если книга не найдена, выбрасываем ошибку

    def find_book_by_id(self, book_id: int) -> Book:
        """
        Ищет книгу по ID.
        Возвращает объект книги, если она найдена, иначе None.
        """
        for book in self.books:
            if book.id == book_id:
                return book
        return  None # Возвращаем None, если книга не найдена

    def search_books(self, query: str, field: str) -> List[Book]:
        """
        Ищет книги по заданному полю (title, author, year).
        Возвращает список книг, которые соответствуют запросу.
        """
        return [book for book in self.books if query.lower() in str(getattr(book, field)).lower()]

    def change_book_status(self, book_id: int, new_status: str):
        """
        Изменяет статус книги.
        Статус должен быть "в наличии" или "выдана". В случае ошибки выбрасывает исключение.
        """
        if new_status not in ["в наличии", "выдана"]:
            raise ValueError("Неверный статус. Возможные значения: 'в наличии', 'выдана'.")
        book = self.find_book_by_id(book_id)
        if book:
            book.status = new_status  # Изменяем статус книги
            self.save_books()  # Сохраняем изменения
        else:
            raise ValueError(f"Книга с ID {book_id} не найдена.")  # Если книга не найдена, выбрасываем ошибку

    def display_books(self) -> List[Dict]:
        """
        Возвращает список всех книг в библиотеке.
        """
        return [book.to_dict() for book in self.books]  # Преобразуем книги в словари и возвращаем список


def main():
    # Главная функция программы, которая управляет меню и взаимодействием с пользователем.
    library = Library()  # Создаем объект библиотеки
    while True:
        # Главное меню
        print("\nМеню:"
              "\n1. Добавить книгу"
              "\n2. Удалить книгу"
              "\n3. Найти книгу"
              "\n4. Показать все книги"
              "\n5. Изменить статус книги"
              "\n0. Выход")
        try:
            choice = input("Выберите действие: ")  # Ввод выбора пользователем
            match choice:
                case "1":
                    # Добавление книги
                    try:
                        print(f'Введите "отмена" для возвращения в меню или')
                        title = input("Введите название книги: ")
                        if title.lower() == "отмена":
                            continue
                        author = input("Введите автора книги: ")
                        year = input("Введите год издания книги: ")
                        if not Book.validate_year(year):
                            raise ValueError("Некорректный год.")
                        library.add_book(title, author, int(year))  # Добавляем книгу в библиотеку
                        print("Книга добавлена!")
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                case "2":
                    # Удаление книги
                    try:
                        book_id = input("Введите ID книги для удаления (или 'назад' для возврата в меню): ").strip()
                        if book_id.lower() == "назад":
                            continue
                        book_id = int(book_id)
                        library.delete_book(book_id)  # Удаляем книгу по ID
                        print("Книга удалена.")
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                case "3":
                    # Поиск книги
                    field = input(
                        "Искать по полю (title, author, year или 'назад' для возврата в меню): ").strip().lower()
                    if field.lower() == "назад":
                        continue
                    if field not in ["title", "author", "year"]:
                        print("Ошибка: некорректное поле для поиска. Попробуйте снова.")
                        continue
                    query = input("Введите запрос (или 'назад' для возврата в меню): ").strip()
                    if query.lower() == "назад":
                        continue
                    results = library.search_books(query=query, field=field)  # Указываем поле для поиска
                    if not results:
                        print("Книги по запросу не найдены.")
                    else:
                        for book in results:
                            print(book.to_dict())
                case "4":
                    # Показать все книги
                    for book in library.display_books():
                        print(book)
                case "5":
                    # Изменение статуса книги
                    try:
                        book_id = input("Введите ID книги: ")
                        if book_id.lower() == "назад":
                            continue
                        book_id = int(book_id)
                        new_status = input("Введите новый статус (в наличии/выдана): ")
                        library.change_book_status(book_id, new_status)
                        print("Статус книги изменен.")
                    except ValueError as e:
                        print(f"Ошибка: {e}")
                case "0":
                    print("Выход из программы.")
                    break
                case _:
                    print("Неверный выбор. Попробуйте снова.")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
