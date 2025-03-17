build:
	docker compose build

run:
	docker compose up

lint:
	ruff format . && ruff check --fix .

bash:
    docker compose exec -ti ip-geolocator bash

makemigrations:
    docker compose exec ip-geolocator alembic revision --autogenerate

migrate:
    docker compose exec ip-geolocator alembic upgrade head

test:
    pytest --cov .