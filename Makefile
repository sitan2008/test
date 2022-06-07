docker-compose:
	docker-compose up -d --remove-orphans --quiet-pull --build app

docker-compose-d:
	docker-compose down
