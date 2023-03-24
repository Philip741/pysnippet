#!/usr/bin/env python
import argparse
import string
import pysnip

parser = argparse.ArgumentParser()

parser.add_argument("--menu", action="store_true")
parser.add_argument("--snippets", action="store_true")
parser.add_argument("--notes" ,action="store_true")
parser.add_argument("--add" ,action="store_true")
#using nargs can add multiple arguments and reference as a list
parser.add_argument("--editnote", nargs=2)
parser.add_argument("--editsnip", nargs='+')
args = parser.parse_args()

if args.menu:
    pysnip.main()
elif args.snippets:
    pysnip.snippet_menu()
elif args.notes:
    pysnip.notes_menu()
elif args.add:
    pysnip.add_text()
elif args.editnote:
    #pysnip.edit_cli(args.edit)
    print(args.editnote[0])
