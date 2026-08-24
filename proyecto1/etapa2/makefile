PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
PROGRAMA = calclex.py
ARCHIVO = prueba.txt

.PHONY: setup run clean clean-all

setup: $(VENV)/.installed

$(VENV)/.installed:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PYTHON) -m pip install --upgrade pip
	$(VENV_PYTHON) -m pip install ply
	touch $(VENV)/.installed

run: setup
	$(VENV_PYTHON) $(PROGRAMA) $(ARCHIVO)

clean:
	rm -f salida_*.txt
	rm -rf __pycache__

clean-all: clean
	rm -rf $(VENV)