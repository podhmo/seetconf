SHELL := $(shell which bash)

default: 00 01

# json
00:
	python -m sheetconf.cli load \
 --config=./config.py:Config \
 --format=json \
 $(shell echo $@*/)config.json \
 |& tee $(shell echo $@*/)output.txt

# csv
01:
	python -m sheetconf.cli load \
 --config=./config.py:Config \
 --format=csv \
 $(shell echo $@*/)config \
 |& tee $(shell echo $@*/)output.txt
