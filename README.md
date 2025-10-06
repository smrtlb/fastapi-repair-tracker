# 🔧 Repair Tracker

Веб-приложение для отслеживания ремонтов и технического обслуживания активов (недвижимость, транспорт, оборудование).

## ✨ Особенности

- 🏠 **Управление активами**: недвижимость, транспорт, оборудование
- 🔧 **Отслеживание ремонтов**: планирование и учет выполненных работ
- 📊 **Статистика и отчеты**: анализ расходов и активности
- 📥 **Импорт/Экспорт данных**: CSV и Excel форматы
- 👤 **Система ролей**: USER и ADMIN
- ⚙️ **Настройки пользователя**: валюта, язык, формат даты, тема
- 📱 **Адаптивный дизайн**: работает на всех устройствах
- 🌙 **Темная тема**: современный интерфейс

## 🚀 Технологии

- **Backend**: FastAPI + SQLite
- **Frontend**: HTML + Jinja2 + Tailwind CSS + JavaScript
- **Аутентификация**: JWT токены
- **База данных**: SQLite
- **Валидация**: Pydantic
- **Файлы**: openpyxl, chardet

## 📋 Требования

- Python 3.8+
- pip

## 🛠️ Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/yourusername/fastapi-repair-tracker.git
cd fastapi-repair-tracker
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Запустите приложение:**
```bash
python main.py
```

4. **Откройте в браузере:**
```
http://localhost:8000
```

## 📖 Использование

### Регистрация и вход
- Зарегистрируйтесь с email и паролем
- Войдите в систему
- Настройте профиль и предпочтения

### Управление активами
- Создайте активы (дом, квартира, автомобиль и т.д.)
- Добавьте описание и тип
- Управляйте списком активов

### Отслеживание ремонтов
- Добавьте ремонт к активу
- Укажите дату, описание, исполнителя
- Отметьте статус (планируется/выполнено)
- Добавьте стоимость и заметки

### Импорт данных
- Скачайте шаблоны CSV с dashboard
- Заполните данные в Excel/LibreOffice
- Импортируйте файлы через dashboard
- Поддерживаются различные форматы дат и стоимости

### Экспорт данных
- Экспортируйте данные в Excel
- Фильтруйте по активам, статусу, году
- Сортируйте по дате или активу

## 📁 Структура проекта

```
fastapi-repair-tracker/
├── main.py                    # Основной FastAPI файл
├── database.py                # Работа с SQLite
├── models.py                  # Pydantic модели
├── auth.py                    # Аутентификация
├── requirements.txt           # Зависимости
├── .gitignore                # Git ignore файл
├── README.md                 # Документация
├── IMPORT_TROUBLESHOOTING.md # Руководство по импорту
├── templates/                # HTML шаблоны
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── assets/
│   └── repairs/
├── static/                   # Статические файлы
│   ├── css/
│   └── js/
└── repair_tracker.db        # База данных (создается автоматически)
```

## 🔧 API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация
- `POST /auth/login` - Вход
- `GET /auth/me` - Текущий пользователь

### Активы
- `GET /api/assets` - Список активов
- `POST /api/assets` - Создание актива
- `GET /api/assets/{id}` - Получение актива
- `PUT /api/assets/{id}` - Обновление актива
- `DELETE /api/assets/{id}` - Удаление актива

### Ремонты
- `GET /api/repairs` - Список ремонтов
- `POST /api/repairs` - Создание ремонта
- `GET /api/repairs/{id}` - Получение ремонта
- `PUT /api/repairs/{id}` - Обновление ремонта
- `DELETE /api/repairs/{id}` - Удаление ремонта

### Экспорт/Импорт
- `GET /api/export/repairs` - Экспорт ремонтов
- `GET /api/export/assets` - Экспорт активов
- `POST /api/import/assets` - Импорт активов
- `POST /api/import/repairs` - Импорт ремонтов
- `GET /api/templates/assets` - Шаблон активов
- `GET /api/templates/repairs` - Шаблон ремонтов

### Профиль
- `GET /api/profile` - Профиль пользователя
- `PUT /api/profile` - Обновление профиля
- `PUT /api/profile/password` - Смена пароля
- `GET /api/profile/settings` - Настройки
- `PUT /api/profile/settings` - Обновление настроек

## 📊 Форматы данных

### Импорт CSV
- **Разделитель**: точка с запятой (;)
- **Кодировка**: UTF-8 (автоматическое определение)
- **Форматы дат**: YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY, DD-MM-YYYY, MM/DD/YYYY, YYYY.MM.DD
- **Форматы стоимости**: 643.36, $150.50, €100.25, 25000 (в центах)

### Пример CSV для активов
```csv
name;type
House on Main Street;PROPERTY
Office Building;PROPERTY
Company Car;VEHICLE
```

### Пример CSV для ремонтов
```csv
asset_name;date;description;performed_by;notes;cost_cents;status
House on Main Street;2024-01-15;Roof repair;John Smith;Fixed leak in roof;643.36;COMPLETED
Office Building;2024-02-10;Heating maintenance;Mike Johnson;Annual service;150.50;COMPLETED
```

## ⚙️ Настройки

### Валюта
- USD ($), EUR (€), RUB (₽), GBP (£), JPY (¥)

### Языки
- English, Русский, Deutsch, Français, Español

### Форматы дат
- DD.MM.YYYY, MM/DD/YYYY, YYYY-MM-DD

### Темы
- Dark (по умолчанию), Light

## 🔒 Безопасность

- Хеширование паролей с bcrypt
- JWT токены с истечением
- Проверка прав доступа
- Валидация всех входных данных
- Защита от SQL инъекций

## 🐛 Устранение неполадок

См. файл [IMPORT_TROUBLESHOOTING.md](IMPORT_TROUBLESHOOTING.md) для решения проблем с импортом данных.

### Частые проблемы:

1. **Ошибка кодировки при импорте**
   - Сохраните файл в UTF-8
   - Используйте правильный разделитель (;)

2. **Неправильный формат даты**
   - Используйте один из поддерживаемых форматов
   - Проверьте правильность даты

3. **Ошибка формата стоимости**
   - Используйте числа (643.36) или целые числа
   - Валютные символы поддерживаются

## 🤝 Вклад в проект

1. Fork репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл `LICENSE` для подробностей.

## 👥 Авторы

- Dan - [smrtlb](https://github.com/smrtlb)

## 🙏 Благодарности

- FastAPI за отличный фреймворк
- Tailwind CSS за красивые стили
- SQLite за простую базу данных
- Cursor за создание приложения

## 📞 Поддержка

Если у вас есть вопросы или проблемы:
- Создайте [Issue](https://github.com/smrtlb/fastapi-repair-tracker/issues)
- Напишите на email: dev@smartlab.fi

---

⭐ Если проект был полезен, поставьте звезду!
