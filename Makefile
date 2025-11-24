PYTHON_VERSION := python3.13
VENV_DIR := .venv

setup:
	if [ ! -d "$(VENV_DIR)" ]; then \
		python3 -m venv $(VENV_DIR); \
		$(VENV_DIR)/bin/pip install --upgrade pip; \
		$(VENV_DIR)/bin/pip install -r requirements.txt; \
	fi

run: 
	nohup $(VENV_DIR)/bin/python main.py > output.log 2>&1 &