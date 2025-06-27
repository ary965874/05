FROM python:3.11

WORKDIR /autofilterbot

COPY . /autofilterbot

RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
