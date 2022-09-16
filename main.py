#!/usr/bin/env python
import argparse
import pysnip

parser = argparse.ArgumentParser()

parser.add_argument("--menu")
parser.add_argument("--snippets", action="store_true")
parser.add_argument("--notes" ,action="store_true")
parser.add_argument("--add" ,action="store_true")
parser.add_argument("--edit")
args = parser.parse_args()

if args.menu:
    pysnip.main()
elif args.snippets:
    pysnip.snippet_menu()
elif args.notes:
    pysnip.notes_menu()
elif args.add:
    pysnip.add_text()
elif args.edit:
    print(args.edit)
