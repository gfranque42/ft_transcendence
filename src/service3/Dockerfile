FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib vim && \
    apt-get clean

WORKDIR /project

COPY ./ /project/

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /project/entrypoint.sh

ENTRYPOINT ["/project/entrypoint.sh"]
