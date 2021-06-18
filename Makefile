PACKAGE = quakeio
VRNPATN = '__version__ = "([^"]+)"'
VERSION = $(shell sed -nE 's:__version__ = "([^"]+)":\1:p' ./src/$(PACKAGE)/__init__.py)
# Documentation
DOCDIR = docs
STYDIR = style
TESTDIR = ~/stdy

PDOC = pdoc --template-dir $(STYDIR) -o $(DOCDIR)


install:
	python3 setup.py develop
	#pip install -e .
cov:
	coverage run --source=. -m pytest
	coverage-badge > ./etc/coverage/cov.svg
test:
	pytest

api:
	$(PDOC) --config show_source_code=False \
	--config latex_math=True \
	--html --force 
	mv $(DOCDIR)/$(PACKAGE)/*.html $(DOCDIR)/api/latest/
	for item in $(DOCDIR)/api/latest/*.html; do mv $$item $${item%.html}.md; done
web:
	elstir build
	/bin/cp -r out/web/* ~/web/quakeio/
	rm ~/web/ana/*.mako

publish:
	python setup.py clean --all sdist bdist_wheel
	twine upload --verbose --skip-existing dist/*
	git tag -a $(VERSION) -m 'version $(VERSION)'
	git push --tags

.PHONY: api

