FROM python:3.7-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app/

CMD ["uvicorn", "app.application:app", "--host", "127.0.0.1", "--port", "8000","--reload"]