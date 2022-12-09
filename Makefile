clean:
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov

coverage:
	coverage run -m pytest
	coverage report

html: coverage
	coverage html

run:
	flask --app raftaar --debug run

db:
	flask -app raftaar init-db

venv:
	python3 -m venv venv

whl:
	python setup.py bdist_wheel

reqs:
	pip freeze > requirements.txt
