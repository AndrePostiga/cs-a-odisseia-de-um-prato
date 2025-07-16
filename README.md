# cs-a-odisséia-de-um-prato

A Python-based game developed for the Computer Science “Games Lab” course.

---

## 📋 Prerequisites

- **Python 3.12**  
- **Git**  
- **Make** & a Unix-style shell (bash, zsh…)

---

## 🚀 Installation

```bash
git clone https://github.com/AndrePostiga/cs-a-odisseia-de-um-prato.git
cd cs-a-odisseia-de-um-prato
make install
```

- **make install**  
  1. Installs Poetry (if missing) and configures a `.venv` in-project  
  2. Installs all runtime and development dependencies from `pyproject.toml`

---

## ▶️ Usage

- **Run the game**  
  ```bash
  make run
  ```
- **Run tests**  
  ```bash
  make test
  ```

---

## 🛠 Development Workflow

- **Lint**  
  ```bash
  make lint
  ```
- **Format**  
  ```bash
  make format
  ```
- **Clean caches**  
  ```bash
  make clean
  ```
- **Build**  
  ```bash
  make build
  ```

---

## 🔍 Run Pre-commit Hooks Manually

You can invoke your pre-commit checks on staged files (or all files) without creating a Git commit:

1. Stage your changes:  
   ```bash
   git add path/to/your_file.py
   ```
2. Run all hooks:  
   ```bash
   poetry run pre-commit run --all-files
   ```
3. Or run a single hook:  
   ```bash
   poetry run pre-commit run black
   poetry run pre-commit run ruff
   ```

---

## 📁 Project Structure

```
.
├── .pre-commit-config.yaml    # pre-commit hook definitions
├── Makefile                   # build & dev commands
├── pyproject.toml             # Poetry configuration
├── poetry.lock                # locked dependency versions
├── src/
│   ├── app/
│   │   ├── __init__.py        # marks package as typed for MyPy
│   │   └── main.py            # game entry point
│   └── tests/
│       └── test_main.py       # pytest tests
├── .gitignore                 # ignore build artifacts & caches
└── LICENSE                    # MIT License
```

---

## 📄 License

This project is licensed under the **MIT License**. See `LICENSE` for details.
