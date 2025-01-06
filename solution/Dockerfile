FROM python:3.12.1-alpine3.19

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV SERVER_PORT=8080

CMD ["sh", "-c", "cd application && python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8080"]