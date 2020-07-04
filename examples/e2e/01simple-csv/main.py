import sys
import sheetconf
from sheetconf.usepydantic import Parser
from config import Config  # ./config.py

filename = sys.argv[1]
config = sheetconf.loadfile(filename, parser=Parser(Config, loader=sheetconf.CSVLoader()))
print(config)
