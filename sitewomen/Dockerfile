FROM python:3.12-slim

# Добавляем группу и пользователя
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj

# Устанавливаем переменные среды
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Обновляем pip
RUN pip install --upgrade pip

# Устанавливаем рабочую директорию
WORKDIR /app/www/sitewomen

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем остальные файлы
COPY . .

# Устанавливаем пользователя
USER userdj