# Описание
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Ключевые возможности сервиса
- Генерация коротких ссылок и связь их с исходными длинными ссылками
- Переадресация на исходный адрес при обращении к коротким ссылкам

Доступны web и api интерфейсы.

## Запуск сервиса
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Ogyrecheg/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл настроек окружения:
```
touch .env
```
Заполнить его:
```
FLASK_APP=yacut
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY = 'MY_SECRET_KEY'
SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
```
Запустить:
```
flask run
```


**Технологии:**
- Python
- Flask
- SQLAlchemy
- Jinja2

### Автор проекта:
[Шевченко Александр](https://github.com/Ogyrecheg)
