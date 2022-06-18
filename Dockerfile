FROM python:latest
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --user

COPY src .
COPY .env .env

CMD ["python", "app.py"]
