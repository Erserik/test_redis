# Используем официальный Python образ
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY . /app/

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Экспонируем порт
EXPOSE 8001

# Запускаем команду для старта сервера
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "test_redis.asgi:application"]
