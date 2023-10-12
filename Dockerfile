FROM python:3.8.18-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app/

CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000","--reload"]