FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы проекта (включая .json)
COPY . .

# Указываем порт (требует хостинг)
EXPOSE 8080

# CMD ["python", "main/run.py"] - было так сначала
CMD ["python", "-m", "main.run"]