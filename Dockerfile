FROM python:3.13-slim
RUN apt update && apt install curl -y && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

HEALTHCHECK --interval=1m --timeout=5s --retries=3 CMD curl --silent --fail http://localhost:8888/health || exit 1

CMD [ "fastapi","run" ]