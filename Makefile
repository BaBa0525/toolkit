VENV = venv
ACTIVATE = ${VENV}/bin/activate
PYTHON = ${VENV}/bin/python3
PIP = ${VENV}/bin/pip

.PHONY: all init clean

all: init

init: ${PIP} requirements.txt
	virtualenv -p python3 ${VENV}
	${PIP} install -r requirements.txt

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
