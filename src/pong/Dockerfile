FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib vim redis-server && \
    apt-get clean

WORKDIR /project

COPY ./requirements.txt /project/

COPY ./entrypoint.sh /project/

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /project/entrypoint.sh

ENTRYPOINT ["bash", "/project/entrypoint.sh"]
