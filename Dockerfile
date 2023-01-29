FROM python:3.9

RUN apt-get update && apt-get install -y cmake python3-pip python3-dev

RUN mkdir /melp_restaurant_api
WORKDIR /melp_restaurant_api

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY poetry.lock pyproject.toml /melp_restaurant_api/
RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY ./app /melp_restaurant_api/app
COPY ./alembic /melp_restaurant_api/alembic
COPY ./alembic.ini /melp_restaurant_api/alembic.ini
COPY ./main.py /melp_restaurant_api/

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
