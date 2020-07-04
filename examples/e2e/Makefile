SHELL := $(shell which bash)

default: 00

00:
	python $(shell echo $@*/)main.py $(shell echo $@*/)config.json |& tee $(shell echo $@*/)output.txt
