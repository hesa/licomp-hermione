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

check_version:
	@echo -n "Checking api versions: "
	@MY_VERSION=`grep api_version licomp_osadl/config.py | cut -d = -f 2 | sed -e "s,[ ']*,,g"` ; LICOMP_VERSION=`grep licomp requirements.txt | cut -d = -f 3 | sed -e "s,[ ']*,,g" -e "s,[ ']*,,g" -e "s,\(^[0-9].[0-9]\)[\.0-9\*]*,\1,g"` ; if [ "$$MY_VERSION" != "$$LICOMP_VERSION" ] ; then echo "FAIL" ; echo "API versions differ \"$$MY_VERSION\" \"$$LICOMP_VERSION\"" ; exit 1 ; else echo OK ; fi

test:
	PYTHONPATH=.: python3 -m pytest --log-cli-level=10 tests/

test-local:
	PYTHONPATH=.:../licomp python3 -m pytest --log-cli-level=10 tests/

install:
	pip install .

reuse:
	reuse lint

check: clean reuse lint test check_version build
	@echo
	@echo
	@echo "All tests passed :)"
	@echo
	@echo
