SHELL := $(shell which bash)

default: 00 01

00:
	python $(shell echo $@*/)main.py $(shell echo $@*/)config.json |& tee $(shell echo $@*/)output.txt
01:
	python $(shell echo $@*/)main.py $(shell echo $@*/)config |& tee $(shell echo $@*/)output.txt
