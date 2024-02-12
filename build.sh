#!/bin/bash

#pyinstaller --onefile --add-data './pysnip/pysnip.cfg:.' cli.py
pyinstaller --onefile --add-data './pysnip/pysnip.cfg:.' pysnip_rel.py
