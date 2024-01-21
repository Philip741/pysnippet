import os.path
import shutil
import errno
import json
import configparser
import subprocess
from sys import platform
import sys
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit import history
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import WordCompleter


def clear_screen():
    """ Clears the screen based on OS """
    name = os.name
    # for windows
    if name == 'nt':
        _ = os.system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
def get_ostype():
    return platform.system

class BaseManager:
    def __init__(self, config, base_path_key):
        self.config = config
        #get section from configparser
        self.base_path = config.get("file_location", base_path_key)
        self.editor_type = config.get("editor", "editor_name")
        self.home_dir = os.path.expanduser("~")  # works on both windows and linux

    def get_categories(self):
        all_files = []
        for root, dirs, files in os.walk(self.base_path):
            for f in files:
                f = f.split('.')
                all_files.append(f[0])
        all_files.sort()
        return all_files

    def get_name(self, category, path) -> list:
        """Returns list of all snippet or note names in json file"""
        name_list = []
        try:
            with open(path + category + ".json", 'r') as f:
                data = json.load(f)
                for k, v in data.items():
                    name_list.append(k)
        except FileNotFoundError:
            print("Snippets not found")
        return name_list

    def retrieve_text(self, category, text_name, path):
        """Returns text from snippet or note name in json file"""
        if category != 'avail':
            try:
                with open(path + category + ".json", 'r') as f:
                    data = json.load(f)
                    print("\n")
                    for k, v in data.items():
                        if k == text_name:
                            for value in v:
                                #print(value)
                                print(value.rstrip())
                                #return value.rstrip()
                        elif text_name == "all":
                            return k
                    print("\n")
                # todo: better capture exception
            except FileNotFoundError:
                print("Snippet not found")


    def search_markdown(self, category, text_name, path):
        pass


    def write_json(self, data, filename):
        # pass in json data using top level key ex. snippets
        # write to filename provided
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)


class SnippetManager(BaseManager):
    CATEGORY_PROMPT = 'category# '
    SNIP_MENU_COMMANDS = ["add", "edit", "exit"]
    SNIPPET_NOT_FOUND = 'Snippet not found'
    CATEGORY_NOT_FOUND = 'Category not found'
    MESSAGE_NO_SNIPPETS = "No snippets in category!"
    MAX_CATEGORY_LENGTH = 32
    def __init__(self, config):
        super().__init__(config, "snippet_location")

    def snippet_menu(self):
        session = PromptSession()
        # get category from base_manager set to category var
        category = self.get_category(session)
        # return if category not found
        if category is None:
            print(self.CATEGORY_NOT_FOUND)
            return
        # get names of all snippets in category
        snippets = self.get_name(category, self.base_path)
        print(snippets)
        completer = WordCompleter(snippets)
        while True:
            snip_prompt = prompt(f'{category}# ', completer=completer)
            if snip_prompt == "exit":
                return
            elif snip_prompt == "edit":
                edit_prompt = prompt(f'snippet name# ', completer=completer)
                self.edit_snippet(category, edit_prompt, self.base_path )
            elif snip_prompt == "add":
                add_snip_name = prompt('New snippet name# ')
                self.add_snippet(category, snippets, add_snip_name)
            elif snip_prompt == "delete":
                delete_snippet = prompt(f'snippet to delete#')
            else:
                self.get_snippet(category, snippets, snip_prompt)


    def edit_snippet(self, category, name, path):
        # gets editor if set in environment var otherwise defaults to editor_type in config
        editor = os.environ.get('EDITOR', self.editor_type)
        # open existing snippet file
        text_content = {}
        with open(path + category + ".json", 'r') as f:
            data = json.load(f)
            # get snippet
            for k, v in data.items():
                if k == name:
                    print(k)
                    text_content = [_ for _ in v]
                    print(text_content)
        # write to tmp file
        with open(path + category + ".tmp", 'w') as f:
            print(text_content)
            for i in text_content:
                f.write(i)
        # open tmp file for editing with editor
        subprocess.call([editor, path + category + ".tmp"])
        # append tmp file snippet back to original file
        with open(path + category + ".tmp", 'r') as f:
            file_lines = [line for line in f]
            tmp_dict = {name: file_lines}
        data.update(tmp_dict)
        self.write_json(data, path + category + ".json")
        # delete tmp file
        os.remove(path + category + ".tmp")

    def get_category(self, session):
        """Returns category name from session input"""
        categories = self.get_categories()
        categ_comp = WordCompleter(categories)
        print("Enter snippet category\n")
        _input = session.prompt(self.CATEGORY_PROMPT, completer=categ_comp, enable_history_search=True)
        if _input in categories and 1 <= len(_input) < self.MAX_CATEGORY_LENGTH:
            return _input.split()[0]
    # get category passes category to input of get_snippet

    def get_snippet(self, category, snippets, name):
        # get_name returns a list of snippet names
        if not snippets:
            print(self.MESSAGE_NO_SNIPPETS)
            return

        if name in snippets:
            snippet_content = self.retrieve_text(category, name, self.base_path)
            #print(snippet_content)
            #return snippet_content
        else:
            print(self.SNIPPET_NOT_FOUND)
            return
    def add_snippet(self, category, snippets, name):
        with open(self.base_path + category + ".json", 'r') as s:
            append_text = json.load(s)
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
                    snippet_dict[name] = snippet_content
                except EOFError:
                    break

            # append newly added text to category file contents
            append_text.update(snippet_dict)
        self.write_json(append_text, self.base_path + category + ".json")

    def delete_snippet(self, category, name):
        with open(self.base_path + category + ".json", 'r') as f:
            data = json.load(f)
            for s in data.keys():
                if s == name:
                    delete_snippet = s
        del data[delete_snippet]
        # open file and write data with key removed
        with open(self.base_path + category + ".json", 'w') as f:
            json.dump(data, f, indent=4)

class NoteManager(BaseManager):
    def __init__(self, config):
        super().__init__(config, "note_location")

    def notes_menu(self):
        # Logic specific for notes
        pass

    # ... additional note-specific methods


class App:
    def __init__(self):
        self.home_dir = os.path.expanduser("~")
        self.config = self.load_config()
        self.snippet_manager = SnippetManager(self.config)
        self.note_manager = NoteManager(self.config)

    # def load_config(self):
    #     current_file_path = os.path.abspath(__file__)
    #     current_directory = os.path.dirname(current_file_path)
    #     source_path = os.path.join(current_directory, "pysnip.cfg")
    #     destination_path = os.path.join(self.home_dir, "pysnip.cfg")
    #     # set pysnip.cfg
    #     shutil.copy(source_path, destination_path)
    #     config = configparser.ConfigParser()
    #     if os.name == 'nt':
    #         config.read_file(open(f"{self.home_dir}\pysnip.cfg"))
    #     else:
    #         config.read_file(open(f"{self.home_dir}/pysnip.cfg"))
    #     return config

    def load_config(self):
        # this is_frozen is used to resolve the path pyinstaller uses
        is_frozen = getattr(sys, 'frozen', False)
        if is_frozen:
            application_path = getattr(sys, '_MEIPASS', os.getcwd())
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        source_path = os.path.join(application_path, "pysnip.cfg")
        destination_path = os.path.join(self.home_dir, "pysnip.cfg")
        if not os.path.exists(destination_path):
            shutil.copy(source_path, destination_path)

        config = configparser.ConfigParser()
        config.read(destination_path)
        return config

    def create_category(self, name, path):
        file_path = path + name + ".json"

        if os.path.exists(file_path):
            print("Category currently exists")
        else:
            with open(file_path, 'w') as s:
                snippet_init = {}
                json.dump(snippet_init, s, indent=4)
    def menu(self):
        # Function to check input at prompt and match
        main_commands = [
            "snippet-categories",
            "note-categories",
            "snippets",
            "notes",
            "new-category",
            "help",
            "exit",
            "clear",
        ]
        while True:
            for index, option in enumerate(main_commands, 1):
                print(f"{index}. {option}")

            choice = prompt("Enter a choice: ")

            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(main_commands):
                    if choice == 3:  # If user selected "snippet-categories"
                        self.snippet_manager.snippet_menu()  # Call the snippet_menu method
                    # exit choice
                    elif choice == 5:
                        category_name = prompt("Enter category name# ")
                        base_path = self.config["file_location"]
                        self.create_category(category_name, base_path.get("snippet_location"))
                    elif choice == 7:
                        return
                    elif choice == 8:
                        clear_screen()
                    # Here you can add elif statements for other choices and implement their functionalities
                    #...
                    #return choice
            else:
                print("Invalid choice, please try again.")
    # ... other utility functions ..

if __name__ == "__main__":
    app = App()
    app.menu()