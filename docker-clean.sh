#!/bin/bash
#docker compose down -v || true
docker stop `docker ps -qa` || true
docker rm `docker ps -qa` || true
#docker rmi -f $(docker images -aq) || true
docker rmi -f `docker images -qa` || true
docker volume rm $(docker volume ls -qf) || true
docker network rm `docker network ls -q` || true
docker system prune -a | printf 'y' || true
docker builder prune | printf 'y' || true

