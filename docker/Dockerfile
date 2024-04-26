FROM python:3.10

WORKDIR /usr/src/b2broker

ENV PYTHONUNBUFFERED 1

COPY . .

RUN ls -la && pwd

RUN pip install poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENTRYPOINT ["./docker/entrypoint.sh"]
