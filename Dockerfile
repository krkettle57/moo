FROM python:3.8 as builder
WORKDIR /usr/src/app
RUN pip install poetry
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry export -f requirements.txt > requirements.txt

FROM python:3.8
ENV PYTHONUNBUFFERED=1
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .
ENTRYPOINT [ "python", "app.py" ]

