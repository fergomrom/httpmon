init: 
	python -m venv httpmon_venv

install: init
	source ./httpmon_venv/bin/activate &&  pip install -r requirements.in && pip install -e .

install-dev: init
	source ./httpmon_venv/bin/activate && pip install -r dev-requirements.in

lint:
	echo "Running isort"
	isort --recursive --diff --quiet --check src tests || exit 1

	echo "Running flake8"
	flake8 --config .flake8.ini src tests || exit 1

	echo "Running pydocstyle"
	pydocstyle || exit 1

test:
	pytest -v tests