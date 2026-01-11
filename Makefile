.PHONY: setup install convert clean help

help:
	@echo "Commandes disponibles:"
	@echo "  make setup    - Crée l'environnement virtuel et installe pandas"
	@echo "  make install  - Installe pandas dans l'environnement virtuel"
	@echo "  make convert  - Exécute le script de conversion JSON vers CSV"
	@echo "  make clean    - Nettoie les données et détecte les anomalies"
	@echo "  make help     - Affiche cette aide"

setup:
	python3 -m venv venv
	./venv/bin/pip install pandas

install:
	./venv/bin/pip install pandas

convert:
	./venv/bin/python convert_to_csv.py

clean:
	./venv/bin/python clean_data.py
