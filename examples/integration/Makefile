SHELL := $(shell which bash)

00:
	python -m sheetconf.cli load $(shell echo $@*/)config.json |& tee $(shell echo $@*/)output.txt
