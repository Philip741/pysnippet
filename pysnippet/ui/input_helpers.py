from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

# all input handling for menus
class InputHandler:
    def __init__(self):
        self.session = PromptSession()

    def get_input(self, prompt_text, completions=None ):
        """Handle user input with prompt_tookit"""
        completer = WordCompleter(completions) if completions else None
        try:
            return self.session.prompt(prompt_text, completer=completer)
        except Exception as e:
            print(f"Warning prompt tookit error {e}")

        
