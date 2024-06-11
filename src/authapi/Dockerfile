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

<<<<<<< HEAD

=======
>>>>>>> 1408063 (👷 build: add new aplication for authentication api)
CMD bash entrypoint.sh
