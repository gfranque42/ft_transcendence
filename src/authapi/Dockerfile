FROM alpine:3.19

RUN apk update

RUN apk add build-base postgresql bash\
	python3-dev py3-pip --no-cache

WORKDIR /project

COPY requirements.txt /project/

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

COPY ./authapi/static/pages/Avatar.jpg /default_avatar.jpg

ENTRYPOINT ["sh", "entrypoint.sh"]
