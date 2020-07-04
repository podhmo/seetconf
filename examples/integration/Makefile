SHELL := $(shell which bash)

default: 00 01 02 03 04 05 10 11

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

# adjust json
02:
	cp $(shell echo $@*/)config.pre.json $(shell echo $@*/)config.json
	python -m sheetconf.cli load \
 --adjust \
 --config=./config.py:Config \
 --format=json \
 $(shell echo $@*/)config.json \
 |& tee $(shell echo $@*/)output.txt
	diff -u $(shell echo $@*/)config.pre.json $(shell echo $@*/)config.json \
 |& tee $(shell echo $@*/)a.diff || exit 0

# adjust csv
03:
	rm -rf $(shell echo $@*/)config
	cp -r $(shell echo $@*/)config.pre $(shell echo $@*/)config
	python -m sheetconf.cli load \
 --adjust \
 --config=./config.py:Config \
 --format=csv \
 $(shell echo $@*/)config \
 |& tee $(shell echo $@*/)output.txt
	diff -ru $(shell echo $@*/)config.pre $(shell echo $@*/)config \
 |& tee $(shell echo $@*/)a.diff || exit 0

# adjust json (missing field)
04:
	cp $(shell echo $@*/)config.pre.json $(shell echo $@*/)config.json
	python -m sheetconf.cli load \
 --adjust \
 --config=./config.py:Config \
 --format=json \
 $(shell echo $@*/)config.json \
 |& tee $(shell echo $@*/)output.txt
	diff -u $(shell echo $@*/)config.pre.json $(shell echo $@*/)config.json \
 |& tee $(shell echo $@*/)a.diff || exit 0

# adjust csv (missing field)
05:
	rm -rf $(shell echo $@*/)config
	cp -r $(shell echo $@*/)config.pre $(shell echo $@*/)config
	python -m sheetconf.cli load \
 --adjust \
 --config=./config.py:Config \
 --format=csv \
 $(shell echo $@*/)config \
 |& tee $(shell echo $@*/)output.txt
	diff -ru $(shell echo $@*/)config.pre $(shell echo $@*/)config \
 |& tee $(shell echo $@*/)a.diff || exit 0

# init json
10:
	python -m sheetconf.cli init \
 --config=./config.py:Config \
 --format=json \
 $(shell echo $@*/)config.json


# init csv
11:
	python -m sheetconf.cli init \
 --config=./config.py:Config \
 --format=csv \
 $(shell echo $@*/)config

