# О проекте
## Маленькое приложение на Python, содержащее пару эндпоинтов: для сокращения ссылки и для перехода по ней. 

# Технологии 
#### ● Python 3.12+ 
#### ● sqlite3 (стандартная библиотека, без ORM) 
#### ● pytest 
#### ● FastApi
#### ● Poetry 

# Эндпоинты 
#### 1. POST /shorten Принимает длинную ссылку Возвращает короткий URL 
#### 2. GET /{code} Делает редирект

# Использование
### Создание виртуального окружения
```bash
  run python -m venv venv
```
```bash
  source venv/bin/activate
```
### Для Windows: 
```bash
  venv\Scripts\activate
```
### Установка зависимостей
```bash
  pip install poetry
```
```bash
  poetry install
```

### Запуск локально

Создать файл .env в корневой директории и добавить переменную BASE_URL со значением "http://localhost:8000"
### Команда для запуска приложения

```bash
  uvicorn app.main:app --reload
```

# Тесты
#### Команда для запуска тестов 

```bash
  pytest ./tests/test_shorten.py
```


