PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
PROGRAMA = calclex.py
ARCHIVO = input/prueba.txt
DUMPS = ../etapa2/input

.PHONY: setup run run-dump clean clean-all

setup: $(VENV)/.installed

$(VENV)/.installed:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install ply
	touch $(VENV)/.installed

run: setup
	$(VENV_PYTHON) $(PROGRAMA) $(ARCHIVO)

CHUNK = chunk_aa.txt
run-dump: setup
	$(VENV_PYTHON) $(PROGRAMA) $(DUMPS)/$(CHUNK)

clean:
	rm -rf output
	rm -rf __pycache__

clean-all: clean
	rm -rf $(VENV)