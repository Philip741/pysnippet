#!/bin/env python


# author: Philip Browning

import os
import json
import configparser
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
print(snippet_path)

def main():
    ''' Function to check input at prompt and match'''
    main_commands = ['category','help','clear','add','delete','snippets','new-category']
    #snippet directory check and create if absent
    #load config file

    while(True):
        menu = main_menu(main_commands)
        #print(menu)
        if menu == "exit":
            break

def main_menu(main_commands):

    session = PromptSession()
    categ_comp = WordCompleter(main_commands)
    print("\n")
    text_input = session.prompt('Main-menu# ',completer = categ_comp)
    command = text_input

    if command == 'category':
        snip_category = get_categories()
        for c in snip_category:
            print(c)

    elif command == 'help':
        print('show help here')

    elif command == 'snippets':
        snippet_menu()

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
    categories = get_categories()
    snip_list = []
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
        snips = compl_snippets(cat_input[0])
        if len(snips) == 0:
            return
        print(f"List of snippets {snips}")
        snip_complete = WordCompleter(snips)
        print("Enter snippet name\n")
        while(True):
            snip_prompt = session.prompt(f'{cat_input[0]}# ', completer = snip_complete)
            if snip_prompt in snips:
                search(cat_input[0], snip_prompt)
            elif snip_prompt == "exit":
                break
            else:
                print("Snippet not found")

def search(category,snippet=''):
    if category != 'avail': 
        try:
            with open('snippets/' + category + ".json", 'r') as f:
                data = json.load(f)    
                for s in data:
                    for k,v in s.items():
                        if k == snippet:
                            for value in v:
                                print("\n" + value + "\n")
                        elif snippet == "all":
                            print("\n" + k)
        except:
            print("Snippet not found")

def strip_input(str_input):
    pass

def add_snippet(category):
    snippet_name = prompt("Enter snippet name: ")
    with open('snippets/' + category + ".json", 'r') as s:
        #snippet_input function to enter snippet text
        snippet_text = snippet_input(snippet_name)
        # load file into append_snip
        append_snip = json.load(s)
        # append newly added text to category file contents
        append_snip.append(snippet_text)
    write_json(append_snip,'snippets/' + category + ".json")

def del_snippet(category, snippet):
    with open('snippets/' + category + ".json", 'r') as f:
        data = json.load(f)    
        #flatten list to dict
        snippet_dict = {key: value for s in data for key, value in s.items()}

        for s in snippet_dict.keys():
            if s == snippet:
                del_key = s

    del snippet_dict[del_key]
    #open file and write data with key removed
    with open('snippets/' + category + ".json", 'w') as f:
        snippet_list = []
        snippet_list.append(snippet_dict)
        json.dump(snippet_list,f, indent=4)    


def edit_snippet():
    pass

def search_snip():
    '''Search snippets after entering category'''
    print("Search Snippet Category\n")
    snipname =  input("Enter snippet category: ")
    if snipname == 'avail':
        return get_categories()
    
    print("Enter snippet name or all(for all snippet names)") 
    snippet = input("Enter snippet name: ")
    try:
        with open('snippets/' + snipname + ".json", 'r') as f:
            data = json.load(f)    
            for s in data:
                for k,v in s.items():
                    #print(k,v)
                    if k == snippet:
                        for value in v:
                            print(value)
                    elif snippet == "all":
                        print(k)
    except:
        print("Could not find snippet name")

def get_categories():
#    '''Returns a list of all category files'''
    all_files = []
    snippets_dir = snippet_path
    for root,dirs,files  in os.walk(snippets_dir):
        for f in files:
            f = f.split('.')
            all_files.append(f[0])
    return all_files       

def compl_snippets(category):
    '''Returns list of all snippets in categories json file'''
    snip_list = []
    try:
        with open('snippets/' + category + ".json", 'r') as f:
            data = json.load(f)    
            for s in data:
                x = s
                for k,v in s.items():
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
    file_path = 'snippets/' + name + ".json"

    if os.path.exists(file_path):
        print("Category currently exists")
    else:
        with open(file_path, 'w') as s:
            snippet_init = []
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


bindings = KeyBindings()
# key bindings
@bindings.add('c-s')
def _(event):
    " Search when `c-s` is pressed. "
    run_in_terminal(snippet_menu())

if __name__ == '__main__':
    main()

