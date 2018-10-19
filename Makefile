init:
	pip install -r requirements.txt

flake8:
	flake8

test:
	pytest tests

run:
	python3 example.py
