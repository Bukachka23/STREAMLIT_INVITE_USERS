FROM python:3.11-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

ENTRYPOINT ["streamlit", "run"]

CMD ["src/main.py"]