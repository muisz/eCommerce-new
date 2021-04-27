FROM python:3.7

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt