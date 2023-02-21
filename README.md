# QRKot

<details>
  <summary>Содержание</summary>
  <ul>
    <li>
      <a href="#описание">Описание</a>
      <ul>
        <li><a href="#-возможности">Возможности</a></li>
        <li><a href="#технологии">Технологии</a></li>
      </ul>
    </li>
    <li>
      <a href="#-начало-работы">Начало работы</a>
      <ul>
          <li><a href="#-зависимости">Зависимости</a></li>
          <li><a href="#установка">Установка</a></li>
          <li><a href="#локальный-запуск-development">Локальный запуск</a></li>
      </ul>
    </li>
    <li><a href="#-использование">Использование</a></li>
    <li><a href="#автор-проекта-ilya-petrukhin">Автор проекта</a></li>
  </ul>
</details>

<a name="описание"></a>

Благотворительный фонд поддержки котиков.
Фонд собирает пожертвования на различные целевые проекты:
на медицинское обслуживание нуждающихся хвостатых,
на обустройство кошачьей колонии в подвале,
на корм оставшимся без попечения кошкам — на любые цели,
связанные с поддержкой кошачьей популяции.

### 🔥 Возможности

- В Фонде QRKot может быть открыто несколько целевых проектов.
- Каждый пользователь может сделать пожертвование и сопроводить его
  комментарием.
- Пожертвования в проекты поступают по принципу **First In**, **First Out**.

### Технологии

[![FastAPI][FastAPI-badge]][FastAPI-url]
[![FastAPIUsers][FastAPIUsers-badge]][FastAPIUsers-url]
[![SQLAlchemy][SQLAlchemy-badge]][SQLAlchemy-url]
[![pre-commit][pre-commit-badge]][pre-commit-url]

## ⚙ Начало Работы

Чтобы запустить локальную копию проекта, следуй инструкциям ниже.

### ⚠ Зависимости

- [Python 3.7+][Python-url]

### Установка

1. **Клонируй репозиторий**

   ```shell
   git clone https://github.com/tvules/QRKot.git
   cd QRKot
   ```

### Локальный Запуск (Development)

1. **Установи зависимости проекта**

    ```shell
    pip install -r requirements.txt
    ``` 
2. **В корне проекта создай `.env` файл**

    ```dotenv
    SECRET="<секретный ключ>"
    ```

   **Секретный ключ можно сгенерировать [тут](https://djecrety.ir/)*

3. **Запусти локальный сервер**

    ```shell
    uvicorn app.main:app
    ```

   После запуска, проект будет доступен по адресу http://localhost:8000/

## 👀 Использование

**Swagger UI** доступен по адресу http://localhost:8000/docs.

Там ты найдешь полную документацию к **API**, а также сможешь сделать запрос на
сервер.

---

<h4 align="center">
Автор проекта: <a href="https://github.com/tvules">Ilya Petrukhin</a>
</h4>

[Python-url]: https://www.python.org/

[FastAPI-badge]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi

[FastAPI-url]: https://fastapi.tiangolo.com/

[FastAPIUsers-badge]: https://img.shields.io/badge/FastAPI%20Users-ef5552?style=for-the-badge

[FastAPIUsers-url]: https://fastapi-users.github.io/fastapi-users

[SQLAlchemy-badge]: https://img.shields.io/badge/sqlalchemy-fbfbfb?style=for-the-badge

[SQLAlchemy-url]: https://www.sqlalchemy.org/

[pre-commit-badge]: https://img.shields.io/badge/pre--commit-1f2d23?style=for-the-badge&logo=pre-commit&logoColor=FAB040

[pre-commit-url]: https://pre-commit.com/
