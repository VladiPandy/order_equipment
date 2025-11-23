FROM python:3.10-slim

WORKDIR /request_bot

RUN mkdir -p logs && chmod 755 logs

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot/ ./bot/

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "bot.main"]

