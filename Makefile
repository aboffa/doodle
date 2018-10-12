HERE = $(shell pwd)
VENV = ~/.local/pyvenv-ase
BIN = $(VENV)/bin
PYTHON = $(BIN)/python

.PHONY: all run test

all: run

run:
	FLASK_APP=myservice $(BIN)/flask run

test:
	$(BIN)/pytest ${HERE}
