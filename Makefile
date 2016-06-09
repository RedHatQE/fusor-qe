#
#
# $Id: f0907aa8b3da8fc0c71c2fffc05f10def5b608fe $
#
.PHONY: 2to3 coverage docs init install lint test

2to3:
	echo futurize
	echo caniusepython3 --project
	echo pylint --py3k
	echo tox

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

lint:
	echo pylint
	echo flake8
    
test:
	echo py.test tests

#
#
#