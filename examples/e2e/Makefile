SHELL := $(shell which bash)

default: 00 01 10

# json
00:
	python $(shell echo $@*/)main.py $(shell echo $@*/)config.json |& tee $(shell echo $@*/)output.txt

# csv
01:
	python $(shell echo $@*/)main.py $(shell echo $@*/)config |& tee $(shell echo $@*/)output.txt

# spreadsheet
10: SHEET_URL := "https://docs.google.com/spreadsheets/d/1PgLfX5POop6QjpgjDLE9wbSWWXJYcowxRBEpxmpG8og"
10:
	python $(shell echo $@*/)main.py $(SHEET_URL) |& tee $(shell echo $@*/)output.txt
