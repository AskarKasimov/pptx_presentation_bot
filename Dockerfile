FROM python:3.11
WORKDIR ./
ARG BOT_TOKEN
ENV BOT_TOKEN $BOT_TOKEN
COPY ./ ./
RUN ["pip", "install", "-r", "requirements.txt"]
ENTRYPOINT ["python3", "main.py"]