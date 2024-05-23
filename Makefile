COMPOSE		= ./srcs/docker-compose.yml

COMPOSE_CMD = docker-compose -f ${COMPOSE}

build:
	@${COMPOSE_CMD} up --build

up:
	@${COMPOSE_CMD} up

down:
	@${COMPOSE_CMD} down

re: down
	@${COMPOSE_CMD} up --build

clean: down
	@docker system prune -a

fclean: down clean
	@docker stop $$(docker ps -qa)
	@docker system prune --all --force --volumes
	@docker network prune --force
	@docker volume prune --force

.PHONY: build up down re clean fclean