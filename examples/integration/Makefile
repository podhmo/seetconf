SHELL := $(shell which bash)

default: 00 01 10 11

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

# json
10:
	python -m sheetconf.cli init \
 --config=./config.py:Config \
 --format=json \
 $(shell echo $@*/)config.json

# csv
11:
	python -m sheetconf.cli init \
 --config=./config.py:Config \
 --format=csv \
 $(shell echo $@*/)config

