FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["sh", "-c", "streamlit run src/main.py --server.port=$PORT --server.address=0.0.0.0"]