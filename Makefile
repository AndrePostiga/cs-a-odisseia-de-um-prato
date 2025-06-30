POETRY := $(HOME)/.local/bin/poetry
POETRY_URL := https://install.python-poetry.org

.PHONY: setup install run shell test lint format typecheck clean

setup:
	@echo "🔍 Checking for Poetry installation..."
	@if ! command -v poetry &>/dev/null; then \
		echo "📦 Poetry not found. Installing Poetry..."; \
		curl -sSL $(POETRY_URL) | python3 -; \
	else \
		echo "✅ Poetry is already installed."; \
	fi
	@echo "⚙️  Configuring Poetry..."
	$(POETRY) config virtualenvs.in-project true
	@echo "🔧 Creating virtual environment..."
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
		$(POETRY) env use .venv/bin/python; \
	fi
	@echo "✅ Setup completed."

install: setup
	@echo "📥 Installing dependencies..."
	$(POETRY) install

run:
	@echo "🚀 Running the application..."
	$(POETRY) run python src/app/main.py

test:
	@echo "🧪 Running tests..."
	$(POETRY) run pytest src/tests/

lint:
	@echo "🧹 Linting code..."
	$(POETRY) run ruff check .

format:
	@echo "✨ Formatting code..."
	$(POETRY) run black .
	$(POETRY) run ruff format .

typecheck:
	@echo "🔎 Checking types..."
	$(POETRY) run mypy src/

clean:
	@echo "🗑 Cleaning caches and temp files..."
	@find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	@rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache .coverage .venv 
