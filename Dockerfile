FROM python:3.8 as builder

WORKDIR /app

COPY . .

RUN pip install pipenv

RUN pipenv install --deploy

CMD STAGE=PRODUCTION pipenv run prod
