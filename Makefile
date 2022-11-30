.PHONY: uninstall_requirements
uninstall_requirements:
	pip freeze --exclude-editable | xargs pip uninstall -y

.PHONY: upgrade_requirements
upgrade_requirements:
	pip install --upgrade pip setuptools wheel & pip install --upgrade -r requirements.txt

.PHONY: reinstall_requirements
reinstall_requirements: uninstall_requirements upgrade_requirements

.PHONY: outdated
outdated:
	pip list -o

.PHONY: format
format:
	isort . & black .

.PHONY: lint
lint:
	flake8 & isort . --check & black . --check

.PHONY: precommit
precommit: format lint
