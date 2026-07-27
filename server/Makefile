.PHONY: lint quick_lint

lint:
	poetry run ruff check --fix .
	poetry run ruff format .

quick_lint:
	git diff --cached --name-only --diff-filter=ACM --relative -- '*.py' | xargs -r poetry run ruff check --fix
	git diff --cached --name-only --diff-filter=ACM --relative -- '*.py' | xargs -r poetry run ruff format
