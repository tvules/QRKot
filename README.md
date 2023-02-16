# QRKot — Благотворительный фонд поддержки котиков

QRKot - Фонд собирает пожертвования на различные целевые проекты:
на медицинское обслуживание нуждающихся хвостатых,
на обустройство кошачьей колонии в подвале,
на корм оставшимся без попечения кошкам — на любые цели,
связанные с поддержкой кошачьей популяции.

## Особенности

- В Фонде QRKot может быть открыто несколько целевых проектов.
- Каждый пользователь может сделать пожертвование и сопроводить его комментарием.
- Пожертвования в проекты поступают по принципу First In, First Out

## Технологии

- [Python 3.7+](https://www.python.org)
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/)

## Инструкция

**1. Клонируйте репозиторий**

```shell
git clone https://github.com/tvules/cat_charity_fund.git
cd cat_charity_fund
```

**2. Установите зависимости проекта**

```shell
pip install -r requirements.txt
```

**3. В корне проекта создайте `.env` файл**

```shell
APP_TITLE="QRKot"
DESCRIPTION="Благотворительный фонд поддержки котиков QRKot"
SECRET="<your secret key>"
```

*Секретный ключ можно сгенерировать [тут](https://djecrety.ir/)

**4. Запустите сервер**

```shell
uvicorn app.main:app
```

<h5 align="center">Автор проекта: <a href="https://github.com/tvules">Ilya Petrukhin</a></h5>
