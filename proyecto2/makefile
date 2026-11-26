# En Windows el comando es python y en Linux python3
ifeq ($(OS),Windows_NT)
PYTHON = python
else
PYTHON = python3
endif

TECNICA = mrv
ARCHIVO = input/sudoku_9x9_1.txt
SEGUNDOS = 30

.PHONY: menu run

# Abre el menu con las corridas de la exposicion
menu:
	$(PYTHON) menu.py

# Corre una sola tecnica, por ejemplo: make run TECNICA=recocido ARCHIVO=input/sudoku_16x16_2.txt SEGUNDOS=10
run:
	$(PYTHON) main.py $(TECNICA) $(ARCHIVO) $(SEGUNDOS)
