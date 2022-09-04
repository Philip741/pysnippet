#!/bin/env python

# author: Philip Browning

import os
import json
import configparser
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from itertools import chain

config = configparser.ConfigParser()
config.read_file(open('pysnip.cfg'))    
snippet_path = config.get('file_location','snippet_location')
notes_path = config.get('file_location','note_location')

def main():
    ''' Function to check input at prompt and match'''
    main_commands = ['snippet-categories','note-categories','help','edit','clear','add','delete','snippets','notes','new-category']
    #snippet directory check and create if absent
    #load config file

    while(True):
        menu = main_menu(main_commands)
        if menu == "exit":
            break

def main_menu(main_commands):

    session = PromptSession()
    categ_comp = WordCompleter(main_commands)
    print("\n")
    text_input = session.prompt('Main-menu# ',completer = categ_comp)
    command = text_input

    if command == 'note-categories':
        snip_category = get_categories(notes_path)
        for c in snip_category:
            print(c)

    elif command == 'snippet-categories':
        snip_category = get_categories(snippet_path)
        for c in snip_category:
            print(c)

    elif command == 'help':
        print('The available main menu commands are: ')
        for c in main_commands:
            print(c)

    elif command == 'snippets':
        snippet_menu()

    elif command == 'notes':
        notes_menu()

    elif command == 'delete':
        category_name = input("Input category: ")
        snippet_name = input("snippet to delete: ")
        del_snippet(category_name, snippet_name)

    elif command == 'clear':
        clear_screen()

    elif command == 'add':
        categories = get_categories()
        categ_comp = WordCompleter(categories)
        category_prompt = session.prompt("category: ", completer = categ_comp)
        add_snippet(category_prompt) 

    elif command == 'edit':
        categories = get_categories()
        categ_comp = WordCompleter(categories)
        category_prompt = session.prompt("category: ", completer = categ_comp)
        snippet_name = input("snippet to edit: ")
        edit_snippet(category_prompt, snippet_name) 

    elif command == 'new-category':
        category_prompt = session.prompt("new category name: ")
        create_category(category_prompt)

    elif command == 'exit':
        session.output.flush()
        menu_output = "exit"
        return menu_output

    else:
       if len(text_input) == 0:
         pass

def snippet_menu():
    session = PromptSession()
    categories = get_categories(snippet_path)
    #snip_list = []
    categ_comp = WordCompleter(categories)
    print("Enter snippet category\n")
    cat_input = session.prompt('category# ',completer = categ_comp)
    if cat_input in categories:
        cat_input = cat_input.split()
    else:
        print('Category not found')
        return

    if len(cat_input) >= 1 and len(cat_input) < 32 :
        #populate list of snippets based on category
        snips = compl_snippets(cat_input[0],snippet_path)
        if len(snips) == 0:
            return
        print(f"List of snippets {snips}")
        snip_complete = WordCompleter(snips)
        print("Enter snippet name\n")
        while(True):
            snip_prompt = session.prompt(f'{cat_input[0]}# ', completer = snip_complete)
            if snip_prompt in snips:
                search(cat_input[0], snip_prompt,snippet_path)
            elif snip_prompt == "exit":
                break
            else:
                print("Snippet not found")

def notes_menu():
    session = PromptSession()
    categories = get_categories(notes_path)
    categ_comp = WordCompleter(categories)
    print("Enter Note category\n")
    cat_input = session.prompt('category# ',completer = categ_comp)
    if cat_input in categories:
        cat_input = cat_input.split()
    else:
        print('Category not found')
        return

    #populate list of notes based on category
    snips = compl_snippets(cat_input[0],notes_path)
    if len(snips) == 0:
        return
    print(f"List of notes {snips}")
    snip_complete = WordCompleter(snips)
    print("Enter note name\n")
    while(True):
        snip_prompt = session.prompt(f'{cat_input[0]}# ', completer = snip_complete)
        if snip_prompt in snips:
            search(cat_input[0], snip_prompt,notes_path)
        elif snip_prompt == "exit":
            break
        else:
            print("Note not found")

def search(category,snippet, path):
    if category != 'avail': 
        try:
            with open(path + category + ".json", 'r') as f:
                data = json.load(f)    
                print("\n")
                for k,v in data.items():
                    if k == snippet:
                        for value in v:
                            print(value)
                    elif snippet == "all":
                        print("\n" + k)
                print("\n")
            #better capture exception
        except:
            print("Snippet not found")

def add_snippet(category):
    snippet_name = prompt("Enter snippet name: ")
    with open(snippet_path + category + ".json", 'r') as s:
        #snippet_input function to enter snippet text
        snippet_text = snippet_input(snippet_name)
        # load file into append_snip
        append_snip = json.load(s)
        # append newly added text to category file contents
        append_snip.update(snippet_text)
    write_json(append_snip,snippet_path + category + ".json")

def del_snippet(category, snippet):
    with open(snippet_path + category + ".json", 'r') as f:
        data = json.load(f)    
        #flatten list to dict
        #snippet_dict = {key: value for s in data for key, value in s.items()}
        for s in data.keys():
            if s == snippet:
                del_key = s

    del data[del_key]
    #open file and write data with key removed
    with open(snippet_path + category + ".json", 'w') as f:
        json.dump(data,f, indent=4)    

def edit_snippet(category, snippet):
    editor = os.environ.get('EDITOR','vim')
    #open existing snippet file
    with open(snippet_path, 'r') as f:
        data = json.load(f)    
        print(f"data first open in edit_snippet {data}")
    #get snippet
        for k,v in data.items():
            print("edit snippet function for loop")
            if k == snippet:
                for value in v:
                    edit_snippet = value
    #write snippet to tmp file
    with open(snippet_path + category + ".tmp", 'w') as f:
        f.writelines(edit_snippet)
    #delete original snippet from file
    #del_snippet(category, snippet)
    # open tmp file for editing with editor
    subprocess.call([editor,snippet_path + category + ".tmp"])
    #append tmp file snippet back to original file
    with open(snippet_path + category + ".tmp", 'r') as f:
        snippet_lines = [l for l in f]
        tmp_dict = {snippet:snippet_lines}
    data.update(tmp_dict)
    print(f"data with changes {data}")
    write_json(data, snippet_path)
        # delete tmp file
    os.remove(snippet_path + category + ".tmp")

def get_categories(path):
#    '''Returns a list of all category files'''
    all_files = []
    for root,dirs,files  in os.walk(path):
        for f in files:
            f = f.split('.')
            all_files.append(f[0])
    all_files.sort()
    return all_files       

def compl_snippets(category,path):
    '''Returns list of all snippets in categories json file'''
    print(category)
    snip_list = []
    try:
        with open(path + category + ".json", 'r') as f:
            data = json.load(f)    
            for k,v in data.items():
                snip_list.append(k)
    except:
        print("Snippets not found")
    return snip_list
    
def write_json(data, filename):
# pass in json data using top level key ex. snippets
# write to filename provided
    with open(filename,'w') as f:
        json.dump(data,f, indent=4)    

def create_category(name):
    file_path = snippet_path + name + ".json"

    if os.path.exists(file_path):
        print("Category currently exists")
    else:
        with open(file_path, 'w') as s:
            snippet_init = {}
            json.dump(snippet_init,s, indent=4)

def snippet_input(snip_name):
    snippet_content = []
    snippet_dict = {}
    print("To save press enter for new line and")
    print("type ctrl d or ctrl z on windows to exit")
    print("Input snippet: ")
    while(True):
        try:
            line = prompt("# ")
            line = line.rstrip()
            snippet_content.append(line)
            #create key with snip_name and value is list of snippet content
            snippet_dict[snip_name] = snippet_content
        except EOFError:
            return snippet_dict
            break
    

def clear_screen(): 
    ''' Clears the screen based on OS '''
    name = os.name
    # for windows 
    if name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 


#bindings = KeyBindings()
# key bindings

if __name__ == '__main__':
    main()

