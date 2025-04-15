#!/bin/env python3

# author: Philip Browning

import os
import shutil
import errno
import json
import configparser
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
#from prompt_toolkit import history
#from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter

#todo get config file path 
config = configparser.ConfigParser()
config.read_file(open('pysnip.cfg'))
snippet_path = config.get('file_location', 'snippet_location')
print(f"snippet path {snippet_path}")
notes_path = config.get('file_location', 'note_location')
#todo check both snippet and notes paths
editor_type = config.get('editor', 'editor_name')
home_dir = os.path.expanduser("~")

#todo: create function detect OS and set home_dir var
def check_os():
    pass

def set_config():
    current_file_path = os.path.abspath(__file__)
    current_directory = os.path.dirname(current_file_path)
    source_path = os.path.join(current_directory, "pysnip.cfg")
    destination_path = os.path.join(home_dir, "pysnip.cfg")
    # set pysnip.cfg
    shutil.copy(source_path, destination_path)
    
def set_dirs():
    snip_home = f"{home_dir}/.snippets"
    notes_home = f"{home_dir}/.notes"
    print(f'snippet_path: {snippet_path}')
    print(f'snip_home: {snip_home}')
    print(f'os.path.exists(snip_home): {os.path.exists(snip_home)}')
    if not snippet_path and os.path.exists(snip_home):
        try:
            print("Creating snippet in snip_home")
            os.makedirs(snip_home)
            
            #os.path.join(home_dir, snip_home)
        except OSError as ose:
            if ose.errno != errno.EEXIST:
                raise
            pass
    # if snippet_path set and folder not created
    elif snippet_path and not os.path.exists(snippet_path):
        print("Snippet directory does not exist from config. Creating directory")
        try:
            print("will try create snippet dir")
            #os.makedirs(snippet_path)
        except OSError as ose:
            if ose.errno != errno.EEXIST:
                raise
            pass
    if not notes_path and not os.path.exists(notes_home):
        try:
            print(notes_home)
            #os.makedirs(notes_home)
            #os.path.join(home_dir, notes_path)
        except OSError as ose:
            if ose.errno != errno.EEXIST:
                raise
            pass
    # if path set and folder does not exist
    elif notes_path and not os.path.exists(notes_path):
        print("Notes directory does not exist from config. Creating directory")
        try:
            #os.makedirs(notes_path)
            #os.path.join(home_dir, notes_path)
            print(notes_path)
        except OSError as ose:
            if ose.errno != errno.EEXIST:
                raise
            pass

def menu():
    ''' Function to check input at prompt and match'''
    main_commands = ['snippet-categories', 'note-categories', 'help', 'edit', 'exit', 'clear', 'add', 'delete',
                     'snippets', 'notes', 'new-category']
    # snippet directory check and create if absent

    # load config file

    while True:
        menu = main_menu(main_commands)
        if menu == "exit":
            break


def main_menu(main_commands):
    # assigned not used
    #prompthistory = history.InMemoryHistory()
    session = PromptSession()
    categ_comp = WordCompleter(main_commands)
    print("\n")
    text_input = session.prompt('Main-menu# ', completer=categ_comp)
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
        # Todo: complete note name to delete
        cat_type = input("Type either \"note\" or \"snippet\" to choose type to delete: ")
        if cat_type == "note":
            categories = get_categories(notes_path)
            categ_comp = WordCompleter(categories)
            category_prompt = session.prompt("category: ", completer=categ_comp, enable_history_search=True)
            note_name = input("note to delete: ")
            del_snippet(category_prompt, note_name, notes_path)

        elif cat_type == "snippet":
            categories = get_categories(snippet_path)
            categ_comp = WordCompleter(categories)
            category_prompt = session.prompt("category: ", completer=categ_comp)
            snippet_name = input("snippet to delete: ")
            del_snippet(category_prompt, snippet_name, snippet_path)
        else:
            print("Error in input please enter type to delete")

    elif command == 'clear':
        clear_screen()

    elif command == 'add':
        # todo move this into add function
        add_text()

    elif command == 'edit':
        cat_type = input("Type to edit enter \"note\" or \"snippet\": ")
        if cat_type == "note":
            categories = get_categories(notes_path)
            categ_comp = WordCompleter(categories)
            category_prompt = session.prompt("category: ", completer=categ_comp)
            notes = compl_snippets(category_prompt, notes_path)
            print(len(notes))
            notes_list = WordCompleter(notes)
            if len(notes) == 0:
                print("No notes in category!")
                return
            # print(f"List of notes {notes}")
            note_name = session.prompt('note name# ', completer=notes_list)
            # name = input("note to edit: ")
            edit_snippet(category_prompt, note_name, notes_path)
        elif cat_type == "snippet":
            categories = get_categories(snippet_path)
            categ_comp = WordCompleter(categories)
            print(snippet_path)
            category_prompt = session.prompt("category: ", completer=categ_comp, enable_history_search=True)
            snips = compl_snippets(category_prompt, snippet_path)
            if len(snips) == 0:
                print("No snippets in this category!")
                return
            snip_compl = WordCompleter(snips)
            # print(f"List of notes {snips}")
            snip_name = session.prompt('snip name# ', completer=snip_compl)
            edit_snippet(category_prompt, snip_name, snippet_path)

    elif command == 'new-category':
        # todo make cat_type into a function
        cat_type = input("Type of category to add input \"note\" or \"snippet\": ")
        category_prompt = session.prompt("New category name: ")

        if cat_type == "note":
            create_category(category_prompt, notes_path)
        elif cat_type == "snippet":
            create_category(category_prompt, snippet_path)
        else:
            print("Please enter note or snippet for category type")

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
    categ_comp = WordCompleter(categories)
    print("Enter snippet category\n")
    cat_input = session.prompt('category# ', completer=categ_comp, enable_history_search=True)
    if cat_input in categories:
        cat_input = cat_input.split()
    else:
        print('Category not found')
        return

    if len(cat_input) >= 1 and len(cat_input) < 32:
        # populate list of snippets based on category
        snipmenu_commands = ["add", "edit", "exit"]
        snips = compl_snippets(cat_input[0], snippet_path)
        if len(snips) == 0:
            print("No snippets in category!")
            return
        # Add menu commands to the completion list
        all_completions = snips + snipmenu_commands
        snip_complete = WordCompleter(all_completions)
        # print("Enter snippet name\n")
        while True:
            snip_prompt = session.prompt(f'{cat_input[0]}# ', completer=snip_complete)

            if snip_prompt in snips:
                search(cat_input[0], snip_prompt, snippet_path)
            elif snip_prompt == "exit":
                exit()
            elif snip_prompt == "back":
                return # return to previous menu
            # todo Add new snippet and edit while in this category
            elif snip_prompt == "add":
                pass
            elif snip_prompt == "edit":
                pass
            else:
                print("Snippet not found")


def notes_menu():
    session = PromptSession()
    categories = get_categories(notes_path)
    categ_comp = WordCompleter(categories)
    print("Enter Note category\n")
    cat_input = session.prompt('category# ', completer=categ_comp, enable_history_search=True)
    if cat_input in categories:
        cat_input = cat_input.split()
    else:
        print('Category not found')
        return

    # populate list of notes based on category
    # todo change name snips var
    snips = compl_snippets(cat_input[0], notes_path)
    if len(snips) == 0:
        print("No notes in category!")
        return
    snip_complete = WordCompleter(snips)
    print("\nEnter note name\n")
    while (True):
        snip_prompt = session.prompt(f'{cat_input[0]}# ', completer=snip_complete)
        if snip_prompt in snips:
            search(cat_input[0], snip_prompt, notes_path)
        elif snip_prompt == "exit":
            break
        else:
            print("Note not found")


def search(category, snippet, path):
    if category != 'avail':
        try:
            with open(path + category + ".json", 'r') as f:
                data = json.load(f)
                print("\n")
                for k, v in data.items():
                    if k == snippet:
                        for value in v:
                            print(value.rstrip())
                    elif snippet == "all":
                        print(k)
                print("\n")
            # better capture exception
        except:
            print("Snippet not found")


def add_text():
    session = PromptSession()
    cat_type = input("Type of category to add input \"note\" or \"snippet\": ")
    if cat_type == "note":
        path = notes_path
        text_type = "note"
    elif cat_type == "snippet":
        path = snippet_path
        text_type = "snippet"
        # text_name = prompt("Enter snippet name: ")
    else:
        print("Please enter snippet or note")
    categories = get_categories(path)
    categ_comp = WordCompleter(categories)
    category = session.prompt("category to add to: ", completer=categ_comp)
    text_name = prompt(f"Enter new {text_type} name: ")

    with open(path + category + ".json", 'r') as s:
        # snippet_input function to enter snippet text
        new_text = snippet_input(text_name)
        # load file into append_snip
        append_text = json.load(s)
        # append newly added text to category file contents
        append_text.update(new_text)
    write_json(append_text, path + category + ".json")


def del_snippet(category, name, path):
    with open(path + category + ".json", 'r') as f:
        data = json.load(f)
        # flatten list to dict
        # snippet_dict = {key: value for s in data for key, value in s.items()}
        for s in data.keys():
            if s == name:
                del_key = s

    del data[del_key]
    # open file and write data with key removed
    with open(path + category + ".json", 'w') as f:
        json.dump(data, f, indent=4)


def edit_snippet(category, name, path):
    editor = os.environ.get('EDITOR', editor_type)
    # open existing snippet file
    with open(path + category + ".json", 'r') as f:
        data = json.load(f)
        # get snippet
        for k, v in data.items():
            if k == name:
                print(k)
                text_content = [_ for _ in v]
    # write to tmp file
    with open(path + category + ".tmp", 'w') as f:
        for i in text_content:
            f.write(i)
    # delete original snippet from file
    # del_snippet(category, snippet)
    # open tmp file for editing with editor
    subprocess.call([editor, path + category + ".tmp"])
    # append tmp file snippet back to original file
    with open(path + category + ".tmp", 'r') as f:
        file_lines = [line for line in f]
        tmp_dict = {name: file_lines}
    data.update(tmp_dict)
    write_json(data, path + category + ".json")
    # delete tmp file
    os.remove(path + category + ".tmp")


def edit_cli(type, name):
    # Edit notes from command line flag --edit name 
    if type == "note":
        # find note to get category
        # with open(notes_path + category + ".json", 'r') as f:
        pass
    elif type == "snippet":
        pass
    else:
        print("Not a valid type set note or snippet")


def get_categories(path):
    #    '''Returns a list of all category files'''
    all_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            f = f.split('.')
            all_files.append(f[0])
    all_files.sort()
    return all_files


def compl_snippets(category, path):
    '''Returns list of all snippets in categories json file'''
    snip_list = []
    try:
        with open(path + category + ".json", 'r') as f:
            data = json.load(f)
            for k, v in data.items():
                snip_list.append(k)
    except:
        print("Snippets not found")
    return snip_list


def write_json(data, filename):
    # pass in json data using top level key ex. snippets
    # write to filename provided
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def create_category(name, path):
    file_path = path + name + ".json"

    if os.path.exists(file_path):
        print("Category currently exists")
    else:
        with open(file_path, 'w') as s:
            snippet_init = {}
            json.dump(snippet_init, s, indent=4)


def snippet_input(snip_name):
    snippet_content = []
    snippet_dict = {}
    print("To save press enter for new line and")
    print("type ctrl d or ctrl z on windows to save and exit")
    print("Text Input: ")
    while True:
        try:
            line = prompt("# ")
            # line = line.rstrip()
            snippet_content.append(line + "\n")
            # create key with snip_name and value is list of snippet content
            snippet_dict[snip_name] = snippet_content
        except EOFError:
            return snippet_dict



def clear_screen():
    ''' Clears the screen based on OS '''
    name = os.name
    # for windows 
    if name == 'nt':
        _ = os.system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')


if __name__ == '__main__':
    set_dirs()
    #set_config()
    menu()
    

