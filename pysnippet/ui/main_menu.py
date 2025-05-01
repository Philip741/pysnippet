from .snippet_menu import SnippetMenu
from ..managers.content_manager import ContentManager
from .input_helpers import InputHandler

class MainMenu:
    def __init__(self, content_manager, input_handler, snippet_menu):
        self.content_manager = content_manager
        # menu handlers initialization
        self.input_handler = input_handler
        self.snippet_menu = snippet_menu

        self.commands = {
            "help":" - Display this help",
            "exit":" - Exit the program",
            "clear":" - Clear the screen",
            "add-category":" - Add new snippet category",
            "snippets":" - Enter submenu to enter snippet category and access snippets",
            "snippet-categories":"Display all available snippet categories",
            "search-all":" - Search all snippets and categories"
        }

    def menu_run(self):
        """Display and handle the main menu"""

        # main menu loop
        while True:
            main_command = self.input_handler.get_input("Main menu# ", list(self.commands.keys()))
            # command handling
            if main_command == "exit":
                exit()
            elif main_command == "help":
                self.display_help()
            elif main_command == "snippets":
                self.snippet_menu.menu_display(self.input_handler)
            elif main_command == "clear":
                self.content_manager.clear_screen()
            elif main_command == "add-category":
                category_name = self.input_handler.get_input("New categry name: ")
                self.content_manager.add_category(category_name)
            elif main_command == "search-all":
                query = self.input_handler.get_input("Input search term: ")
                if query:
                    results = self.content_manager.search_snippets(query)

                    if results:
                        print(f"\nFound {len(results)} matching snippets:\n")
                        # enumerate results so user can choose one by number if wanted
                        for i, result in enumerate(results, 1):
                            print(f"{i}. {result['category']} > {result['name']}")
                            print(f"   Preview: {result['preview']}")
                            print()
                            
                        # Option to view a result
                        choice = self.input_handler.get_input("Enter number to view (or 'back' to return): ")
                        if choice.isdigit() and 1 <= int(choice) <= len(results):
                            result = results[int(choice) - 1]
                            self.snippet_menu.display_snippet(result['category'], result['name'])
                    else:
                        print(f"No snippets found containing '{query}'.")
                
            elif main_command == "snippet-categories":
                categories = self.content_manager.get_categories()
                if categories:
                    print("\nAvailable categories:")
                    for category in categories:
                        print(f"  {category}")
                else:
                    print("No categories found.")

    def display_help(self):
        for key,val in self.commands.items():
            print(key,val)
