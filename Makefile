.PHONY: build run

build:
	docker compose build

run:
	docker compose up

lint:
	ruff format . && ruff check --fix .