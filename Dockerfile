FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY src /app

EXPOSE 5000
CMD ["python3", "main.py"]