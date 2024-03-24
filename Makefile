all: 
	docker compose -f ./docker-compose.yml build
	docker compose -f ./docker-compose.yml up -d

logs:
	docker logs db
	docker logs backend

clean:
	docker container stop backend db

fclean: clean
	@docker system prune -af

re: fclean all

.Phony: all logs clean fclean