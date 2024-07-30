all: up

up:
	@bash ./host.sh ./src/pong/pong/settings.py
	docker-compose -f ./src/docker-compose.yml up -d --build

v:
	docker-compose -f ./src/docker-compose.yml --verbose up -d --build

stop:
	docker-compose -f ./src/docker-compose.yml stop

down:
	docker-compose -f ./src/docker-compose.yml down

logs:
	# docker-compose -f ./src/docker-compose.yml logs
	bash ./logs.sh

ps:
	docker-compose -f ./src/docker-compose.yml ps

clean: stop

fclean: clean down
	docker system prune -af

re: fclean all

.PHONY: up stop down clean fclean all logs v ps
