.PHONY: ci ci_server ci_client

ci: ci_server ci_client

ci_server:
	cd server && poetry run ruff check . --fix
	cd server && poetry run pytest

ci_client:
	cd client && npm run lint
	cd client && npm run test:unit
