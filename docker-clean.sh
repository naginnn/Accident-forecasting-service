#!/bin/bash
docker compose down -v || true
docker rmi -f $(docker images -aq) || true
docker system prune -a | printf 'y' || true
