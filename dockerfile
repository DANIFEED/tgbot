FROM python:3.10-slim
ENV TOKEN='token from @BotFather'
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "tgbot.py"]
