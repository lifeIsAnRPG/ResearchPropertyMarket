FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

CMD ["gunicorn","--bind 0.0.0.0:80", "app:server"]