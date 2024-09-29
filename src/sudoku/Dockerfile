FROM alpine:3.19

RUN apk update

RUN apk add build-base postgresql bash \
	python3-dev py3-pip redis --no-cache doas

WORKDIR /project

COPY ./entrypoint.sh /project/

COPY ./requirements.txt /project/

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]
