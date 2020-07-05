import sys
import sheetconf
from config import Config  # ./config.py

filename = sys.argv[1]
config = sheetconf.loadfile(filename, config=Config, format="json")
print(config)
