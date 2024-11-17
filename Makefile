# SPDX-FileCopyrightText: 2024 Henrik Sandklef
#
# SPDX-License-Identifier: GPL-3.0-or-later

clean:
	find . -name "*~" | xargs rm -f
	rm -fr licomp_hermione.egg-info
	rm -fr licomp_hermione-0.1.1
	rm -fr build
	rm -fr licomp_hermione/__pycache__
	rm -fr tests/__pycache__
	rm -f *.csv
	rm -fr dist

lint:
	PYTHONPATH=. flake8 licomp_hermione

.PHONY: build
build:
	rm -fr build && python3 setup.py sdist

test:
	PYTHONPATH=. python3 -m pytest --log-cli-level=10 tests/

install:
	pip install .

reuse:
	reuse lint
