
FROM python:3.13-bookworm

WORKDIR /app

COPY app/requirements.txt ./

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
