.ONESHELL:
VENV_NAME=.venv
PYTHON=python3
PIP=$(VENV_NAME)/bin/pip

.PHONY: virtualenv install

virtualenv:
	@echo "Creating virtualenv ..."
	@rm -rf $(VENV_NAME)
	@$(PYTHON) -m venv $(VENV_NAME)
	@$(PIP) install -U pip
	@echo "Virtual environment created."
	@make install

install:
	@echo "Installing dependencies ..."
	@$(PIP) install -r requirements.txt
	@echo "Dependencies installed."
	@echo "!!!Activate the virtual environment by running: source $(VENV_NAME)/bin/activate"

run:
	@echo "Running main.py"
	@$(PYTHON) main.py