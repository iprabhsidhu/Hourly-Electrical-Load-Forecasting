SHELL = /usr/bin/bash
PYTHON = ./venv/bin/python
PIP = ./venv/bin/pip

venv:
	python3 -m venv venv
	source venv/bin/activate

.PHONY: help setup install train test clean
help:
	@echo "Commands"
	@echo "setup : Setup the environment"
	@echo "install : Install dependencies"
	@echo "mlflow : runs the mlflow server"
	@echo "train : Run training pipeline for model"
	@echo "test : Test the model"
	@echo "clean : Remove cache files"

setup :
	python3 -m venv venv

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

mlflow:
	 mlflow server --default-artifact-root file:/home/iprabhsidhu/EnergyPrediction/Models/

train : 
	@echo "Training the model..."
	$(PYTHON) -m main --mode train

test:
	# TODO

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
