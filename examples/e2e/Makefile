SHELL := $(shell which bash)

default: 00 01 02 03 10

# load json
00:
	python $(shell echo $@*/)main.py $(shell echo $@*/)config.json |& tee $(shell echo $@*/)output.txt

# load csv
01:
	python $(shell echo $@*/)main.py $(shell echo $@*/)config |& tee $(shell echo $@*/)output.txt

# dump init
02:
	python $(shell echo $@*/)main.py |& tee $(shell echo $@*/)output.txt

# dump data
03:
	python $(shell echo $@*/)main.py |& tee $(shell echo $@*/)output.txt

# spreadsheet
10: SHEET_URL := "https://docs.google.com/spreadsheets/d/1PgLfX5POop6QjpgjDLE9wbSWWXJYcowxRBEpxmpG8og"
10:
	python $(shell echo $@*/)main.py $(SHEET_URL) |& tee $(shell echo $@*/)output.txt
