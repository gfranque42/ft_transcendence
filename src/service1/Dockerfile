FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib vim && \
    apt-get clean

WORKDIR /project

COPY requirements.txt /project/requirements.txt

COPY entrypoint.sh /project/entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /project/entrypoint.sh

ENTRYPOINT ["bash", "/project/entrypoint.sh"]
