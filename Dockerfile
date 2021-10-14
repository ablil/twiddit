FROM python:latest
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --user

COPY *.py ./
COPY credentials.json credentails.json

CMD ["python", "app.py"]
