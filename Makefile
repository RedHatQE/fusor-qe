#
#
# $Id$
#
.PHONY: 2to3 coverage docs init install lint test

# TODO: Change from stub to working code
2to3:
	echo futurize
	echo caniusepython3 --project
	echo pylint --py3k
	echo tox

# TODO: Change from stub to working code
coverage:
	echo coverage run --branch -m
	echo coverage report -m 
	echo coverage html

docs:	init
	$(MAKE) --directory=docs html
	
init:
	pip install -r requirements.txt --upgrade

install:
	echo python setup.py install

# TODO: Change from stub to working code
lint:
	echo pylint
	echo flake8
    
# TODO: Change from stub to working code
test:
	echo py.test tests

#
#
#
