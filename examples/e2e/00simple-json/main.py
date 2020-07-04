import sys
import sheetconf
from sheetconf.usepydantic import Parser
from config import Config  # ./config.py

filename = sys.argv[1]
config = sheetconf.load(filename, parser=Parser(Config, loader=sheetconf.JSONLoader()))
print(config)
