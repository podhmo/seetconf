import sys
import sheetconf
from sheetconf.usepydantic import Parser
from sheetconf.usegspread import Loader
from config import Config  # ./config.py

filename = sys.argv[1]
config = sheetconf.load(filename, parser=Parser(Config, loader=Loader()))
print(config)
