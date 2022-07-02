FROM python:3.10-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir --pre -r requirements.txt

COPY main.py .

COPY weatherRequest.py .

ENTRYPOINT ["python3", "main.py"]