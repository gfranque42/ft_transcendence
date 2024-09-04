FROM python:3.12.3-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    apt-get clean

WORKDIR /project

COPY requirements.txt /project/requirements.txt

COPY entrypoint.sh /project/entrypoint.sh


RUN pip install -r requirements.txt

RUN chmod +x /project/entrypoint.sh

# WORKDIR /project/media/images/

# WORKDIR /project/media/

# RUN mkdir -p /project/media/images/

COPY ./authapi/static/pages/Avatar.jpg /default_avatar.jpg

ENTRYPOINT ["bash", "/project/entrypoint.sh"]
