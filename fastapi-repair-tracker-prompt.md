# 🐍 Промт для создания Repair Tracker на FastAPI + SQLite

## 📋 Контекст проекта

Создай веб-приложение "Repair Tracker" на **FastAPI + SQLite** с точно такой же функциональностью, как в существующем Next.js проекте. Это приложение для отслеживания ремонтов и технического обслуживания активов. Активом может быть как объект недвижимого (дом, квартира, гараж, склад и тд.), так и движимого имущества (автомобиль, мотоцикл, велосипед и тд.).
Язык проекта по умолчанию английский. 

## 🎯 Основные требования

### **Стек технологий:**
- **Backend**: FastAPI + SQLite
- **Frontend**: HTML + Jinja2 + Tailwind CSS + Vanilla JavaScript
- **Аутентификация**: JWT токены
- **Размер проекта**: Максимум 25 МБ

### **Структура проекта:**

```
repair-tracker/
├── main.py                    # Основной FastAPI файл
├── database.py                # Работа с SQLite
├── models.py                  # Pydantic модели
├── auth.py                    # Аутентификация
├── requirements.txt           # Зависимости
├── templates/                 # HTML шаблоны
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html         # Главная страница с импортом
│   ├── profile.html           # Профиль пользователя
│   ├── assets/
│   │   ├── list.html
│   │   ├── new.html
│   │   ├── detail.html
│   │   └── edit.html
│   └── repairs/
│       ├── list.html
│       ├── new.html
│       └── edit.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── favicon.ico
├── repair_tracker.db          # SQLite база данных
└── IMPORT_TROUBLESHOOTING.md  # Руководство по устранению проблем
```

## 🗄️ База данных (SQLite)

### **Таблицы:**

#### **Users**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'USER' CHECK (role IN ('USER', 'ADMIN')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Assets**
```sql
CREATE TABLE assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    owner_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users (id) ON DELETE SET NULL
);
```

#### **Repairs**
```sql
CREATE TABLE repairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_id INTEGER NOT NULL,
    date DATE NOT NULL,
    description TEXT NOT NULL,
    performed_by TEXT NOT NULL,
    notes TEXT,
    cost_cents INTEGER DEFAULT 0,
    status TEXT DEFAULT 'COMPLETED' CHECK (status IN ('PLANNED', 'COMPLETED')),
    created_by_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES assets (id) ON DELETE CASCADE,
    FOREIGN KEY (created_by_id) REFERENCES users (id) ON DELETE SET NULL
);
```

## 🔐 Система аутентификации

### **Роли пользователей:**
- **USER**: Видит только свои активы и ремонты
- **ADMIN**: Видит все данные. 

### **API endpoints для аутентификации:**
- `POST /auth/register` - Регистрация
- `POST /auth/login` - Вход
- `POST /auth/logout` - Выход
- `GET /auth/me` - Получение текущего пользователя

## 📱 API Endpoints

### **Assets (Активы):**
- `GET /api/assets` - Список активов (с фильтрацией по владельцу)
- `POST /api/assets` - Создание активов
- `GET /api/assets/{id}` - Получение активов по ID
- `PUT /api/assets/{id}` - Обновление активов
- `DELETE /api/assets/{id}` - Удаление активов

### **Repairs (Ремонты):**
- `GET /api/repairs` - Список ремонтов (с фильтрацией и сортировкой)
- `POST /api/repairs` - Создание ремонта
- `GET /api/repairs/{id}` - Получение ремонта по ID
- `PUT /api/repairs/{id}` - Обновление ремонта
- `DELETE /api/repairs/{id}` - Удаление ремонта

### **Экспорт/Импорт:**
- `GET /api/export/repairs` - Экспорт ремонтов в Excel
- `GET /api/export/assets` - Экспорт активов в Excel
- `POST /api/import/assets` - Импорт активов из CSV
- `POST /api/import/repairs` - Импорт ремонтов из CSV
- `GET /api/templates/assets` - Скачивание шаблона для активов
- `GET /api/templates/repairs` - Скачивание шаблона для ремонтов

### **Профиль и настройки:**
- `GET /api/profile` - Получение профиля пользователя
- `PUT /api/profile` - Обновление профиля
- `PUT /api/profile/password` - Смена пароля
- `GET /api/profile/settings` - Получение настроек
- `PUT /api/profile/settings` - Обновление настроек

### **Административные функции:**
- `GET /api/admin/users` - Управление пользователями (только для админов)

## 🎨 Интерфейс пользователя

### **Дизайн:**
- **Темная тема** (как в оригинале)
- **Адаптивный дизайн** для всех устройств
- **Tailwind CSS** для стилизации
- **Интуитивная навигация** с breadcrumbs
- **Язык проекта по умолчанию английский**, предусмотреть возможность локализации на другие языки.

### **Основные страницы:**

#### **1. Dashboard (`/`)** - ⭐ **ЦЕНТРАЛЬНАЯ СТРАНИЦА ИМПОРТА**
- Статистика по ремонтам (с правильным отображением валюты)
- **Карточка импорта данных** с:
  - Скачиванием шаблонов CSV
  - Загрузкой файлов активов и ремонтов
  - Подробными инструкциями по форматам
  - Отображением результатов импорта
- Последние ремонты
- Быстрые действия

#### **2. Assets (`/assets`)**
- Список активов с фильтрацией
- Кнопки "Add Asset", "Edit", "Delete"
- Поиск по названию
- **Экспорт в Excel**
- **БЕЗ кнопки импорта** (перенесено на dashboard)

#### **3. Asset Detail (`/assets/{id}`)**
- Детальная информация о активах
- Список ремонтов для этого актива
- Форма добавления нового ремонта

#### **4. Repairs (`/repairs`)**
- Список всех ремонтов с фильтрацией:
  - По активам (dropdown)
  - По статусу (Planned/Completed)
  - По году (input field)
  - Сортировка по дате/активов (asc/desc)
- Кнопки "Add Repair", "Edit", "Delete"
- **Экспорт в Excel**
- **БЕЗ кнопки импорта** (перенесено на dashboard)

#### **5. Profile (`/profile`)**
- **Основная информация**: имя, email, роль, дата регистрации
- **Смена пароля**: безопасная смена с проверкой текущего
- **Настройки приложения**:
  - Валюта: USD, EUR, RUB, GBP, JPY
  - Язык: English, Русский, Deutsch, Français, Español
  - Формат даты: DD.MM.YYYY, MM/DD/YYYY, YYYY-MM-DD
  - Тема: Dark/Light

#### **6. Forms (Create/Edit)**
- Валидация полей
- Обработка ошибок
- Подтверждение удаления

## 🔧 Технические требования

### **requirements.txt:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
jinja2==3.1.2
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dateutil==2.8.2
openpyxl==3.1.2
pydantic==2.5.0
chardet==5.2.0
```

### **Особенности реализации:**

#### **1. Валидация данных:**
- Использовать Pydantic модели с расширенными валидаторами
- **Поддержка множественных форматов дат**: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, MM/DD/YYYY, YYYY.MM.DD
- **Автоматическое преобразование стоимости**: поддержка десятичных чисел (643.36), валютных символов ($150.50), целых чисел
- Валидация всех входных данных
- Проверка прав доступа

#### **2. Импорт CSV:**
- **Автоматическое определение кодировки** (UTF-8, Windows-1251, Latin1)
- **Разделитель**: точка с запятой (;)
- **Валидация данных** с подробными сообщениями об ошибках
- **Шаблоны для скачивания** с примерами данных
- **Централизованный импорт** на dashboard

#### **3. Фильтрация и сортировка:**
- Query параметры для фильтрации ремонтов
- SQL запросы с WHERE и ORDER BY
- Пагинация (опционально)

#### **4. Экспорт в Excel:**
- Библиотека openpyxl
- Скачивание файлов через FastAPI
- Форматирование данных

#### **5. Безопасность:**
- Хеширование паролей (bcrypt)
- JWT токены для сессий
- Проверка прав доступа на каждом endpoint
- **CORS middleware** для работы с frontend

#### **6. Обработка ошибок:**
- Пользовательские исключения
- HTTP статус коды
- Сообщения об ошибках на русском языке

#### **7. Настройки пользователя:**
- **Отображение валюты** согласно настройкам пользователя
- **Форматирование дат** согласно выбранному формату
- **Многоязычность** интерфейса
- **Темная/светлая тема**

## 📊 Примеры данных

### **Тестовые данные:**
```python
# Пользователи
users = [
    {"email": "admin@example.com", "name": "Admin", "role": "ADMIN"},
    {"email": "user@example.com", "name": "User", "role": "USER"}
]

# Активы
assets = [
    {"name": "House on Main Street", "type": "PROPERTY", "owner_id": 1},
    {"name": "Office Building", "type": "PROPERTY", "owner_id": 1},
    {"name": "Company Car", "type": "VEHICLE", "owner_id": 2}
]

# Ремонты
repairs = [
    {"property_id": 1, "date": "2024-01-15", "description": "Roof repair", "performed_by": "John Smith", "cost_cents": 64336, "status": "COMPLETED"},
    {"property_id": 2, "date": "2024-02-20", "description": "Heating maintenance", "performed_by": "Mike Johnson", "cost_cents": 15050, "status": "PLANNED"}
]
```

## 🚀 Запуск приложения

### **Команды:**
```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск в режиме разработки
python main.py

# Запуск в продакшене
uvicorn main:app --host 0.0.0.0 --port 8000
```

## ✅ Критерии готовности

Проект считается готовым, если:

1. ✅ Все API endpoints работают корректно
2. ✅ Аутентификация и авторизация функционируют
3. ✅ CRUD операции для активов и ремонтов работают
4. ✅ Фильтрация и сортировка ремонтов работают
5. ✅ Экспорт в Excel функционирует
6. ✅ **Импорт CSV работает с различными форматами**
7. ✅ **Настройки пользователя применяются корректно**
8. ✅ **Централизованный импорт на dashboard**
9. ✅ Интерфейс адаптивный и красивый
10. ✅ Размер проекта не превышает 25 МБ
11. ✅ Все функции из оригинального Next.js проекта реализованы

## 📝 Дополнительные требования

- Код должен быть чистым и хорошо документированным
- Использовать type hints везде
- Обработка всех возможных ошибок
- Логирование важных операций
- Готовность к деплою на VPS или хостинг

## 🔗 Дополнительная информация

### **Функциональность из оригинального проекта:**

#### **Управление недвижимостью:**
- Создание, редактирование, удаление активов
- Типы активов: PROPERTY, VEHICLE, EQUIPMENT, etc.
- Связь активов с владельцем

#### **Управление ремонтами:**
- Создание, редактирование, удаление ремонтов
- Статусы: PLANNED, COMPLETED
- Поля: дата, описание, исполнитель, стоимость, заметки
- Связь с недвижимостью и создателем

#### **Система ролей:**
- USER: видит только свои активы
- ADMIN: видит все данные, управление пользователями

#### **Фильтрация и поиск:**
- По активам (dropdown)
- По статусу ремонта
- По году
- Сортировка по дате/активов (asc/desc)

#### **Экспорт и импорт данных:**
- Excel файлы с данными
- **CSV импорт с поддержкой множественных форматов**
- **Автоматическое определение кодировки**
- **Готовые шаблоны для скачивания**
- Фильтрация экспортируемых данных

#### **UI/UX особенности:**
- Темная тема
- Адаптивный дизайн
- Breadcrumb навигация
- Подтверждение удаления
- Состояния загрузки
- Обработка ошибок
- **Централизованный импорт на dashboard**
- **Настройки пользователя с предварительным просмотром**

### **API структура (аналогично Next.js):**

#### **Аутентификация:**
- Регистрация с валидацией email
- Вход с JWT токенами
- Проверка сессий
- Выход из системы

#### **Assets API:**
- GET /api/assets - список с фильтрацией по владельцу
- POST /api/assets - создание
- GET /api/assets/{id} - получение по ID
- PATCH /api/assets/{id} - обновление
- DELETE /api/assets/{id} - удаление

#### **Repairs API:**
- GET /api/repairs - список с фильтрацией и сортировкой
- POST /api/repairs - создание
- GET /api/repairs/{id} - получение по ID
- PATCH /api/repairs/{id} - обновление
- DELETE /api/repairs/{id} - удаление

#### **Экспорт API:**
- GET /api/export/repairs - экспорт ремонтов
- GET /api/export/assets - экспорт активов

#### **Импорт API:**
- POST /api/import/assets - импорт активов из CSV
- POST /api/import/repairs - импорт ремонтов из CSV
- GET /api/templates/assets - шаблон для активов
- GET /api/templates/repairs - шаблон для ремонтов

#### **Профиль API:**
- GET /api/profile - получение профиля
- PUT /api/profile - обновление профиля
- PUT /api/profile/password - смена пароля
- GET /api/profile/settings - получение настроек
- PUT /api/profile/settings - обновление настроек

### **Валидация данных (аналогично Zod схемам):**

```python
# Asset validation
property_create = {
    "name": "required string, min 1 char",
    "type": "required string, enum: PROPERTY, VEHICLE, EQUIPMENT"
}

# Repair validation  
repair_create = {
    "property_id": "required integer, must exist",
    "date": "required date, multiple formats supported",
    "description": "required string, min 1 char",
    "performed_by": "required string, min 1 char",
    "notes": "optional string",
    "cost_cents": "integer, auto-converted from decimal/currency",
    "status": "enum: PLANNED, COMPLETED"
}

# Filter validation
repair_filter = {
    "property_id": "optional integer",
    "status": "optional enum: PLANNED, COMPLETED", 
    "year": "optional integer",
    "sort_by": "optional enum: date, asset",
    "sort_order": "optional enum: asc, desc"
}

# Import validation
import_row = {
    "asset_name": "required string, must exist",
    "date": "required date, multiple formats",
    "description": "required string",
    "performed_by": "required string",
    "notes": "optional string",
    "cost_cents": "integer, auto-converted",
    "status": "enum: PLANNED, COMPLETED"
}
```

### **Безопасность:**
- Хеширование паролей с bcrypt
- JWT токены с истечением
- Проверка прав доступа на каждом endpoint
- Валидация всех входных данных
- Защита от SQL инъекций (параметризованные запросы)
- **CORS middleware** для cross-origin запросов

**Создай полностью функциональное приложение с этой спецификацией!**