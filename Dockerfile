FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    git \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install uv && uv pip install --system .

EXPOSE 5000

CMD ["python", "main.py"]