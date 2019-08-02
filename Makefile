init: 
	python -m venv httpmon_venv

install: init
	source ./httpmon_venv/bin/activate && pip install -e .

install-dev: init
	source ./httpmon_venv/bin/activate && pip install -r dev-requirements.in

clean:
	rm -rf `find . -type d -name ".pytest_cache"`
	rm -rf `find . -type d -name "*.eggs"`
	rm -rf `find . -type d -name "*.egg-info"`
	rm -rf `find . -type d -name "__pycache__"`
	rm -rf `find . -type f -name "*.pyc"`
	rm -rf `find . -type f -name "*.pyo"`

lint:
	echo "Running isort"
	isort --recursive --diff --quiet --check httpmon tests || exit 1

	echo "Running flake8"
	flake8 --config .flake8.ini httpmon tests || exit 1

	echo "Running pydocstyle"
	pydocstyle || exit 1

test:
	pytest -v tests