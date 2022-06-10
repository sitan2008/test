docker-compose:
	docker-compose up -d --remove-orphans --quiet-pull --build app

docker-compose-d:
	docker-compose down

make-deps:
	pipenv sync
	pipenv lock -r > requirements.txt

app:
	python main.py

run: docker-compose


