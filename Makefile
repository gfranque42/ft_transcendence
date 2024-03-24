build:
	docker compose -f ./docker-compose.yml build

up:
	docker compose -f ./docker-compose.yml up -d

down:
	docker compose -f ./docker-compose.yml down

restart:
	make down
	make up

all: build up

clean: down

fclean: clean

re: fclean all

.PHONY: up down clean fclean re