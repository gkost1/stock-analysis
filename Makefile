.PHONY: ci ci_server ci_client makemigrations migrate seed

ci: ci_server ci_client

ci_server:
	cd server && poetry run ruff format .
	cd server && poetry run ruff check . --fix
	cd server && poetry run pytest

ci_client:
	cd client && npm run lint
	cd client && npm run test:unit

makemigrations:
	cd server && poetry run python manage.py makemigrations

migrate:
	cd server && poetry run python manage.py migrate

seed:
	cd server && poetry run python manage.py seed
