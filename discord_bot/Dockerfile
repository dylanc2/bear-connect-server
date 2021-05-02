FROM python:3.7
WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "./quart_discord_bot.py" ]
