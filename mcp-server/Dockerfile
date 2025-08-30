FROM python:3.13-slim

WORKDIR /app

COPY main.py /app
COPY requirements.txt /app
COPY ../.env

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["streamlit", "run", "main.py", "--server.port=8000", "--server.address=0.0.0.0"]