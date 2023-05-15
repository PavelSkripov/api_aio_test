# Базовый образ с python-3.10
FROM python:3.10
# Указание каталога на диске
WORKDIR /app
# Скопируем файл с зависимостями в контейнер
COPY requirements.txt .
# Установим зависимости внутри контейнера
RUN pip install -r requirements.txt
# Скопируем остальные файлы в контейнер
COPY . .

CMD ["python", "-u", "./main.py"]