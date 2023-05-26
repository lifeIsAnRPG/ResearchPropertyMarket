FROM python:3.8-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Запускаем приложение с помощью команды python app.py
CMD ["python", "app.py"]