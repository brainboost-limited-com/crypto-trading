# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /Users/goldenthinker/Projects/crypto_trading/com_goldenthinker_trade_docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]