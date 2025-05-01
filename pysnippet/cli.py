from .ui.main_menu import MainMenu
from .ui.snippet_menu import SnippetMenu
from .managers.content_manager import ContentManager
from .ui.input_helpers import InputHandler
from .config.config import Config


def main():

  main_config = Config()
#  main_config.set_config()
  main_config.set_dirs()  
  main_config.load_config()
  snippet_path = main_config.snippet_path

  # set dependencies
  content_manager = ContentManager(snippet_path)
  input_handler = InputHandler()
  snippet_menu = SnippetMenu()

  #sync_manager = SyncManager (
  #     snippet_path = snippet_path,
  #     sync_config = main_config.get_sync_config(),
  # )
  menu = MainMenu(content_manager,input_handler,snippet_menu)
  menu.menu_run()


if __name__ == "__main__":
    main()
