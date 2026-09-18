PYTHON = python3
VENV = .venv
VENV_PYTHON = $(VENV)/bin/python
PROGRAMA = calclex.py
MAIN = main.py
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
	$(VENV_PYTHON) $(MAIN) $(ARCHIVO)

CHUNK = chunk_aa.txt
run-dump: setup
	$(VENV_PYTHON) $(PROGRAMA) $(DUMPS)/$(CHUNK)

clean:
	rm -rf output
	rm -rf __pycache__

clean-all: clean
	rm -rf $(VENV)

TEST_FILES = archivo.txt registro.txt as_path.txt elemento_as.txt lista_as.txt numero_as.txt prueba.txt

.PHONY: test

test: setup
	@for f in $(TEST_FILES); do \
		echo "==================== $$f ===================="; \
		$(VENV_PYTHON) $(MAIN) input/$$f; \
		echo ""; \
	done