init:
	pip install -r requirements.txt

flake8:
	flake8

test:
	python3 -m pytest tests

run:
	python3 example.py
