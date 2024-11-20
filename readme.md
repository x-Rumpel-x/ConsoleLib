# Система управления библиотекой

Это консольное приложение для управления библиотекой. Оно позволяет пользователям добавлять, удалять, искать, отображать и обновлять статус книг в библиотеке.

## Функции

- **Добавить книгу**: Добавление новой книги в библиотеку с уникальным идентификатором и статусом по умолчанию ``в наличии``.
- **Удалить книгу**: Удаление книги из библиотеки по ее ID. Изящно обрабатывает недействительные вводы.
- **Поиск книги**: Поиск книг по названию, автору или году.
- **Показать все книги**: Показать список всех книг в библиотеке с их подробной информацией (ID, название, автор, год, статус).
- **Изменить статус книги**: Обновление статуса книги (``в наличии`` или ``выдана``) по ее ID.
- **Ведение журнала ошибок**: Все ошибки (например, недействительные идентификаторы, неправильный статус) записываются в файл `error_log.json`.
- **Постоянство данных**: Хранит данные библиотеки в файле `library.json` для сохранения информации между сессиями.

## Требования

- Python 3.x
- Никаких дополнительных библиотек не требуется.

## Использование

1. Клонируйте или загрузите репозиторий.
2. Запустите программу с помощью:
   ``bash
   python app.py


**Книги**: Хранятся в файле `library.json` в следующем формате:
```json
[
    {
        "id": 1,
        "title": "Book Title",
        "author": "Author Name",
        "year": "2024",
        "status": "в наличии"
    }
]
```

***Журналы ошибок***: Хранятся в файле `error_log.json` в следующем формате:
```json
[
    {
        "timestamp": "2024-11-20 12:00:00",
        "error": "Error message"
    }
]
```