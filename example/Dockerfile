FROM python:3.9-slim-buster

WORKDIR /app
COPY ../requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY src /app/src
COPY example/main.py /app/main.py

CMD ["python", "main.py"]

