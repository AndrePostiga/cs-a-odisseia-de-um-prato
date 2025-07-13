# Makefile for cross-platform compatibility (Windows, macOS, Linux)

# OS Detection and Platform-specific commands
ifeq ($(OS),Windows_NT)
    # Windows
    PYTHON := python
    POETRY := poetry
    RM_RF = rmdir /s /q
    DEL_FILE = del /f /q
    CLEAN_PYCACHE = for /d /r . %d in (__pycache__) do @if exist "%d" $(RM_RF) "%d"
    VENV_PATH := .venv\\Scripts\\python
else
    # Unix (macOS, Linux)
    PYTHON := python3
    POETRY := $(HOME)/.local/bin/poetry
    RM_RF = rm -rf
    DEL_FILE = rm -f
    CLEAN_PYCACHE = find . -type d -name "__pycache__" -exec $(RM_RF) {} +
    VENV_PATH := .venv/bin/python
endif

POETRY_URL := https://install.python-poetry.org

.PHONY: setup install run shell test lint format typecheck clean build

setup:
ifeq ($(OS),Windows_NT)
	@echo "🔍 Checking for Poetry installation..."
	@where poetry >nul 2>nul || ( \
		echo "❌ Poetry not found. Please install it for your OS:" && \
		echo "   - Windows (PowerShell): (Invoke-WebRequest -Uri $(POETRY_URL) -UseBasicParsing).Content | $(PYTHON) -" && \
		exit /b 1 \
	)
	@echo "✅ Poetry is already installed."
	@echo "⚙️  Configuring Poetry..."
	$(POETRY) config virtualenvs.in-project true
	@echo "🔧 Creating virtual environment..."
	@if not exist .venv ( \
		$(PYTHON) -m venv .venv && \
		$(POETRY) env use $(VENV_PATH) \
	)
	@echo "✅ Setup completed."
else
	@echo "🔍 Checking for Poetry installation..."
	@if [ ! -f "$(POETRY)" ]; then \
		echo "❌ Poetry not found. Please install it for your OS:"; \
		echo "   - macOS / Linux: curl -sSL $(POETRY_URL) | $(PYTHON) -"; \
		exit 1; \
	fi
	@echo "✅ Poetry is already installed."
	@echo "⚙️  Configuring Poetry..."
	$(POETRY) config virtualenvs.in-project true
	@echo "🔧 Creating virtual environment..."
	@if [ ! -d ".venv" ]; then \
		$(PYTHON) -m venv .venv; \
		$(POETRY) env use $(VENV_PATH); \
	fi
	@echo "✅ Setup completed."
endif

install: setup
	@echo "📥 Installing dependencies..."
	$(POETRY) install

run:
	@echo "🚀 Running the application..."
	$(POETRY) run $(PYTHON) src/app/main.py

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

build:
	@echo "📦 Building game for distribution..."
	-@$(DEL_FILE) "A Odisseia de um Prato.spec"
	-@$(RM_RF) dist
	-@$(RM_RF) build
	$(POETRY) run pyinstaller --name "A Odisseia de um Prato" --windowed --add-data "assets:assets" src/app/main.py

clean:
ifeq ($(OS),Windows_NT)
	@echo "🗑 Cleaning caches and temp files (Windows)..."
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist .ruff_cache rmdir /s /q .ruff_cache
	@if exist .mypy_cache rmdir /s /q .mypy_cache
	@if exist .coverage rmdir /s /q .coverage
	@if exist .venv rmdir /s /q .venv
	@if exist dist rmdir /s /q dist
	@if exist build rmdir /s /q build
	@if exist "A Odisseia de um Prato.spec" del /f /q "A Odisseia de um Prato.spec"
else
	@echo "🗑 Cleaning caches and temp files (Unix)..."
	-@find . -type d -name "__pycache__" -exec rm -rf {} +
	-@rm -rf .pytest_cache .ruff_cache .mypy_cache .coverage .venv dist build
	-@rm -f "A Odisseia de um Prato.spec"
endif
