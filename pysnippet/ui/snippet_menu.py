from ..managers.content_manager import ContentManager
from .input_helpers import InputHandler
from ..config.config import Config
import pyperclip
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


class SnippetMenu:
    def __init__(self, content_manager=None, input_handler=None):
        main_config = Config()
        self.content_manager = ContentManager(main_config.snippet_path)
        self.input_handler = InputHandler()

        # Initialize the rich console
        self.console = Console()
        
        self.commands = {
                'add': 'Add a new snippet to this category',
                'edit': 'Edit a snippet in this category',
                'delete': 'Delete a snippet from this category',
                'back': 'Return to main menu',
                'exit': 'Exit the application'
        }
    def menu_display(self, input_handler):
        """Handle snippet menu interaction"""
        categories = self.content_manager.get_categories()

        if not categories:
            print("No snippet categories found")
            return
        category = input_handler.get_input('snip_category# ', categories)

        # go to main menu
        if not category or category == 'back':
            return
        # get snippets in category
        snippets = self.content_manager.get_items(category)
        # return if user typed in invalid snippet category or command
        if snippets is None:
            return
        # Add commands for navigation
        commands = ["back", "exit", "add", "edit", "delete"]
        all_options = snippets + commands

        while True:
            #populate snippet names in category
            choice = input_handler.get_input(f"{category}# ", all_options)

            if choice == "back":
                return
            elif choice == "exit":
                exit(0)
            elif choice == "clear":
                self.content_manager.clear_screen()
            elif choice == "edit":
                snippet_choice = input_handler.get_input("Choose a snippet to edit# ", snippets)
                self.content_manager.edit_item(category, snippet_choice)
            elif choice == "delete":
                snippet_delete = input_handler.get_input("Choose a snippet to delete# ", snippets)
                self.content_manager.delete_item(category, snippet_delete)
            elif choice == "add":
                snippet_name = input_handler.get_input("Enter name for a new snippet# ")
                if snippet_name:
                    self.content_manager.add_item(category, snippet_name, input_handler)
                # refresh snippets list
                snippets = self.content_manager.get_items(category)
                all_options = snippets + commands
            elif choice in snippets:
                self.display_snippet(category, choice)

    def extract_code_for_clipboard(self, content_text):
        """Extract code content from markdown code blocks"""
        code_lines = []
        in_code_block = False
        
        for line in content_text:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
            elif in_code_block:
                code_lines.append(line)
        return '\n'.join(code_lines)

    def display_snippet(self,category, snippet_name):
        paste_text = []
        # get snippet content returns snippet content from item name value in data dict 
        content = self.content_manager.get_item_content(category, snippet_name)
        if content:
            content_text = ''.join(content)
            
            # Display with Rich markdown formatting
            markdown = Markdown(content_text)
            self.console.print(Panel(
                markdown, 
                title=f"📝 {snippet_name}", 
                border_style="blue"
            ))

            choice = self.input_handler.get_input("Copy code blocks to clipboard y/n: ")
            if choice.lower() == 'y':
                for line in content:
                    if '#tags' in line:
                        pass
                    else:
                        paste_text.append(line)
                full_text = self.extract_code_for_clipboard(paste_text)
                pyperclip.copy(full_text)
                print("Copied to clipboard")

                

