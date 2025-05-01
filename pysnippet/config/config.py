# config.py
import os
import shutil
import configparser

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.home_dir = os.path.expanduser("~")
        self.config_path = os.path.join(self.home_dir, ".pysnippet", "pysnip.cfg")
        
        # Ensure config exists before trying to load it
        self.ensure_config_exists()
        self.load_config()
        
    def ensure_config_exists(self):
        """Make sure the config file exists at the expected location"""
        config_dir = os.path.dirname(self.config_path)
        
        # Create config directory if it doesn't exist
        if not os.path.exists(config_dir):
            try:
                os.makedirs(config_dir)
                print(f"Created config directory: {config_dir}")
            except OSError as e:
                print(f"Error creating config directory: {e}")
                return False
        
        # Check if config file exists
        if not os.path.exists(self.config_path):
            # Find the default config in the package
            package_dir = os.path.dirname(os.path.abspath(__file__))
            default_config = os.path.join(package_dir, "pysnip.cfg")
            
            # If default config exists, copy it
            if os.path.exists(default_config):
                try:
                    shutil.copy(default_config, self.config_path)
                    print(f"Copied default config to {self.config_path}")
                except Exception as e:
                    print(f"Error copying default config: {e}")
                    self.create_default_config()
            else:
                # Create a new default config
                self.create_default_config()
                
        return True
    
    def create_default_config(self):
        """Create a default config file"""
        try:
            self.config["file_location"] = {
                "snippet_location": os.path.join(self.home_dir, ".snippets/")
            }
            self.config["editor"] = {
                "editor_name": os.environ.get('EDITOR', 'nano')
            }
            
            with open(self.config_path, 'w') as f:
                self.config.write(f)
                
            print(f"Created default config at {self.config_path}")
            return True
        except Exception as e:
            print(f"Error creating default config: {e}")
            return False
            
    def load_config(self):
        """Load config from the expected location"""
        try:
            self.config.read(self.config_path)
            self.snippet_path = self.config.get('file_location', 'snippet_location')
            self.editor_type = self.config.get('editor', 'editor_name')
        except Exception as e:
            print(f"Error loading config: {e}")
            # Set defaults if config not loaded correctly
            self.snippet_path = os.path.join(self.home_dir, ".snippets/")
            self.editor_type = os.environ.get('EDITOR', 'nano')
    
    def set_dirs(self):
        """Ensure all required directories exist"""
        dirs_to_check = [
            self.snippet_path
        ]
        
        for directory in dirs_to_check:
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                    print(f"Created directory: {directory}")
                except OSError as e:
                    print(f"Error creating directory {directory}: {e}")
