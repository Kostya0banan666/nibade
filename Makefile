PYTHON := $(shell which python3)
ENV_PATH := $(shell poetry env info -p 2>/dev/null)

install:
	poetry install

shell:
ifndef ENV_PATH
	@echo "Poetry environment not found. Run 'make install' first."
else
	@echo "Activating Poetry env at: $(ENV_PATH)"
	@bash -c "source $(ENV_PATH)/bin/activate && exec bash"
endif

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

createdb:
	poetry run python -c "from app.init_db import ensure_database_exists; ensure_database_exists()"

migrate:
	poetry run python -c "from app.db import Base, engine; Base.metadata.create_all(bind=engine)"

admin:
	PYTHONPATH=./ poetry run python app/scripts/add_admin.py $(ROBLOX_ID)
