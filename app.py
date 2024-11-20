import json
import os


class Book:
    def __init__(self, book_id, title, author, year, status="в наличии"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __repr__(self):
        return f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"


class Library:
    def __init__(self):
        self.books = []
        self.load_books()
        self.load_errors()

    def load_books(self):
        if os.path.exists("library.json"):
            with open("library.json", "r", encoding="utf-8") as file:
                self.books = [Book(**book) for book in json.load(file)]

    def save_books(self):
        with open("library.json", "w", encoding="utf-8") as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

    def load_errors(self):
        if os.path.exists("error_log.json"):
            with open("error_log.json", "r", encoding="utf-8") as file:
                self.error_log = json.load(file)
        else:
            self.error_log = []

    def save_errors(self):
        with open("error_log.json", "w", encoding="utf-8") as file:
            json.dump(self.error_log, file, ensure_ascii=False, indent=4)

    def add_book(self, title, author, year):
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book)
        self.save_books()
        print(f"Книга '{title}' добавлена в библиотеку.")

    def remove_book(self, book_id):
        book = self.find_book_by_id(book_id)
        if book:
            self.books.remove(book)
            self.save_books()
            print(f"Книга с ID {book_id} удалена.")
        else:
            print("Ошибка: книга с таким ID не найдена.")
            self.log_error(f"Книга с ID {book_id} не найдена для удаления.")

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def search_books(self, search_term):
        found_books = [book for book in self.books if search_term.lower() in book.title.lower() or search_term.lower() in book.author.lower() or search_term.lower() in str(book.year)]
        return found_books

    def display_books(self):
        if not self.books:
            print("Библиотека пуста.")
        for book in self.books:
            print(book)

    def change_status(self, book_id, new_status):
        book = self.find_book_by_id(book_id)
        if book:
            if new_status not in ["в наличии", "выдана"]:
                print("Ошибка: Статус может быть только 'в наличии' или 'выдана'.")
                self.log_error(f"Неверный статус для книги с ID {book_id}.")
                return
            book.status = new_status
            self.save_books()
            print(f"Статус книги с ID {book_id} изменён на '{new_status}'.")
        else:
            print("Ошибка: книга с таким ID не найдена.")
            self.log_error(f"Книга с ID {book_id} не найдена для изменения статуса.")

    def log_error(self, error_message):
        self.error_log.append(error_message)
        self.save_errors()


def is_valid_year(year):
    return year.isdigit() and len(year) == 4


def is_valid_name(name):
    return name.isalpha() and len(name) > 1


def main():
    library = Library()

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            print("\nДобавить книгу:")
            title = input("Введите название книги: ")
            while True:
                author = input("Введите имя автора (имя и фамилия): ")
                if is_valid_name(author):
                    break
                print("Ошибка: имя автора должно состоять из букв.")
            while True:
                year = input("Введите год издания: ")
                if is_valid_year(year):
                    break
                print("Ошибка: год должен быть числом и содержать 4 цифры.")
            library.add_book(title, author, int(year))

        elif choice == "2":
            book_id = input("Введите ID книги для удаления: ")
            if book_id.isdigit():
                library.remove_book(int(book_id))
            else:
                print("Ошибка: введён некорректный ID.")

        elif choice == "3":
            search_term = input("Введите название, автора или год для поиска: ")
            results = library.search_books(search_term)
            if results:
                print("\nРезультаты поиска:")
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.display_books()

        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ")
            if book_id.isdigit():
                new_status = input("Введите новый статус (в наличии/выдана): ")
                library.change_status(int(book_id), new_status)
            else:
                print("Ошибка: введён некорректный ID.")

        elif choice == "6":
            print("Выход из программы...")
            break

        else:
            print("Ошибка: неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
