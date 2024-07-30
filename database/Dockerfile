# Use an official Python runtime as a parent image
FROM python:3.10-slim

WORKDIR /app

COPY . /app

# COPY ../schemas /schemas

RUN pip install -r requirements.txt

EXPOSE 8081

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]
