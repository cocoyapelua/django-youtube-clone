FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./app/conf/requirements.txt .
RUN pip install -r requirements.txt

COPY ./app/conf/entrypoint.sh /usr/src/app/conf/entrypoint.sh
RUN sed -i 's/\r$//g' /usr/src/app/conf/entrypoint.sh
RUN chmod +x /usr/src/app/conf/entrypoint.sh

COPY ./app .

ENTRYPOINT ["/usr/src/app/conf/entrypoint.sh"]