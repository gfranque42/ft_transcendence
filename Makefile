all: up

up:
	docker-compose -f ./src/docker-compose.yml up --build

v:
	docker-compose -f ./src/docker-compose.yml --verbose up --build

stop:
	docker-compose -f ./src/docker-compose.yml stop

down:
	docker-compose -f ./src/docker-compose.yml down

log:
	docker-compose -f ./src/docker-compose.yml logs

clean: stop

fclean: clean down
	docker system prune -af

re: fclean all

.PHONY: up stop down clean fclean all log v 