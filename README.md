# Запуск
## Токен бота
Необходимо использовать переменные окружения: поместить в переменную `BOT_TOKEN` токен бота.

Если использовать Docker, то можно создать файл `.env` и записать в него строку следующего формата (после `=` должен идти сам токен):
```
BOT_TOKEN=
```
### Запуск через Docker
```
docker-compose up --build
```
### Запуск без Docker
Установка зависимостей:
```
pip install -r requirements.txt
```
Запуск:
```
python main.py
```
