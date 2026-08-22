#  !"№;!@#$ bot

Telegram-бот на **Aiogram 3** и **SQLAlchemy 2.0** для управления розыгрышами, учетными записями пользователей и автоматизации выдачи бонусов/токенов.

---

## Особенности и функционал

- **Управление пользователями**: Регистрация, привязка профилей (ник/телефон), статусы модерации (`pending`, `approved`, `rejected`).
- **Система токенов**: Учет баланса пользователей для участия в конкурсах.
- **Розыгрыши и конкурсы**:
  - Просмотр активных конкурсов с фото и описанием.
  - Участие в конкурсах в 1 клик через инлайн-кнопки.
  - Просмотр завершенных конкурсов и их победителей.
- **Админ-панель**: Создание конкурсов, управление подписками и базами данных.

---

## Технологический стек

* **Язык**: Python 3.11+
* **Фреймворк бота**: [Aiogram 3.x](https://docs.aiogram.dev/)
* **База данных / ORM**: SQLite + [SQLAlchemy 2.0](https://www.sqlalchemy.org/) (Async)
* **Переменные окружения**: `python-dotenv` / `pydantic-settings`

---

## Структура проекта

```text
nextgen_bot/
│
├── bot/
│   ├── handlers/         # Обработчики команд и меню (admin, client, menu)
│   ├── keyboards/        # Клавиатуры (Reply & Inline)
│   ├── states/           # Состояния FSM
│   └── utils/            # Вспомогательные утилиты и фильтры
│
├── database/
│   ├── db.py             # Настройка асинхронного движка SQLAlchemy
│   ├── models.py         # Описание таблиц БД (User, Contest, ContestUser)
│   └── crud_contest.py   # CRUD-операции для работы с конкурсами и юзерами
│
├── config/               # Загрузка конфигурации из .env
├── main.py               # Точка входа для запуска бота
└── requirements.txt      # Зависимости проекта
```
---

## Быстрый запуск

```text
git clone [https://github.com/fat1m0chka/nextgen_bot.git](https://github.com/fat1m0chka/nextgen_bot.git)
cd nextgen_bot
```
---

## Безопасный запуск

```text
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```
---

## Установка зависимостей

```text
pip install -r requirements.txt
```
---

## Запуск бота

```text
python -m bot.main
```

---
