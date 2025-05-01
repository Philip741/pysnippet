import os
import json
import subprocess
from ..config.config import Config
from ..ui.input_helpers import InputHandler

class ContentManager:
    """ Base class for both snippet and note managers"""

    def __init__(self, path):
        """Returns list of all category files"""
        self.path = path
        self.input_handler = InputHandler()
        self.config = Config()
        self.editor_type = self.config.editor_type

    def get_categories(self):
        """Returns a list of all category files"""
        all_files = []

        if not os.path.exists(self.path):
            print(f"Path not found {self.path}")
            return all_files


        for root, dirs, files in os.walk(self.path):
            for f in files:
                if f.endswith('.json'):
                    category = f.split('.', 1)[0]
                    all_files.append(category)
        all_files.sort()
        return all_files
    
    def get_items(self,category):
        """Get all names in a category"""
        item_list = []
        try:
            with open(f"{self.path}{category}.json") as f:
                data = json.load(f)
                for k,v in data.items():
                    item_list.append(k)
            return item_list

        except FileNotFoundError:
            print(f"Category {category} not found")
            return None


    def get_item_content(self,category,item_name):
        """Get item content"""
        try:
            with open(f"{self.path}{category}.json", 'r') as f:
                data = json.load(f)
            if item_name in data:
                return data[item_name]
            else:
                print(f"Item '{item_name}' not found in category '{category}'")
                return None
        except Exception as e:
            print(f"Error retrieving item: {e}")
            return None

    def edit_item(self, category,name):
        """Edit item content"""
        editor = os.environ.get('EDITOR', self.editor_type)
        file_path = os.path.join(self.path, f"{category}.json")
        temp_path = os.path.join(self.path, f"{category}.tmp")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

                if name not in data:
                    print(f"From edit_item Item '{name}' not found in category '{category}'")
                    return False
                # Get the content
                text_content = data[name]
        
                # Write to temp file
                with open(temp_path, 'w') as f:
                    for line in text_content:
                        f.write(line)
                #open editor
                try:
                    subprocess.call([editor, temp_path])
                except Exception as e:
                    print(f"Error opening editor: {e}")
                    os.remove(temp_path)
                    return False

                with open(temp_path, 'r') as f:
                    file_lines = [line for line in f]

                # update the data
                data[name] = file_lines

                # write the current data back out to file
                self.write_json(data, file_path)

                #cleanup temp file
                os.remove(temp_path)

                return True
            
        except Exception as e:
            print(f"Error editing item: {e}")
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)
            return False

    def delete_item(self, category, name):
        """Delete snippet from file"""
        with open(f"{self.path}{category}.json", 'r') as f:
            data = json.load(f)
            for s in data.keys():
                if s == name:
                    del_key = s
        del data[del_key]
        # write back to snippet file    
        self.write_json(data, f"{self.path}{category}.json")

    def add_category(self, category_name):
        """Add a new category (creates an empty JSON file)"""
        # Ensure safe filename
        safe_name = category_name.strip()

        if not safe_name:
            print("Category name cannot be empty.")
            return False
            
        # Check if category already exists
        file_path = os.path.join(self.path, f"{safe_name}.json")
        
        if os.path.exists(file_path):
            print(f"Category '{safe_name}' already exists.")
            return False
            
        # Create empty JSON file
        try:
            with open(file_path, 'w') as f:
                # Initialize with empty dictionary
                json.dump({}, f, indent=4)
                
            print(f"Category '{safe_name}' created successfully.")
            return True
        except Exception as e:
            print(f"Error creating category: {e}")
            return False


    def add_item(self, category, name, input_handler):
        """Add snippet to category"""
        category_path = os.path.join(self.path, f"{category}.json")
        temp_path = os.path.join(self.path, f"{category}.tmp")
    
        if not os.path.exists(category_path):
            print(f"Category '{category}' does not exist.")
            return False
        
        # Read existing data
        with open(category_path, 'r') as f:
            data = json.load(f)
        
        # Check if name already exists
        if name in data:
            print(f"An item named '{name}' already exists in this category.")
            return False
        
        # Create an empty temp file
        with open(temp_path, 'w') as f:
            f.write("# Enter your snippet content here\n# Lines starting with # are comments and will be included\n\n")
        
        # Get the editor from environment or use default
        editor = os.environ.get('EDITOR', self.editor_type or 'nano')
        
        # Open editor
        try:
            subprocess.call([editor, temp_path])
        except Exception as e:
            print(f"Error opening editor: {e}")
            os.remove(temp_path)
            return False
        
        # Read edited content
        with open(temp_path, 'r') as f:
            file_lines = [line for line in f]
        
        # Add new item
        data[name] = file_lines
        
        # Write updated data
        self.write_json(data, category_path)
        
        # Clean up temp file
        os.remove(temp_path)
        
        print(f"Item '{name}' added successfully to category '{category}'.")
        return True

    def search_snippets(self, query):
        """Search through all snippets"""
        results = []

        # Get all categories
        categories = self.get_categories()

        if not categories:
            print("No categories found to search.")
            return
        print(f"Searching for {query} across all snippets...")

        # Search through each category
        for category in categories:
            snippets = self.get_items(category)
            if not snippets:
                continue

            for snippet_name in snippets:
                content = self.get_item_content(category, snippet_name)
                if not content:
                    continue
                # join content into a single string for searching
                content_text = ''.join(content)
                # add category, name, and snippet text unless it is greater than 50 to results
                if query.lower() in content_text.lower() or query.lower() in snippet_name.lower():
                    results.append({
                    'category': category,
                    'name': snippet_name,
                    'preview': content_text[:50] + '...' if len(content_text) > 50 else content_text
                })
        return results

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
                self.display_snippet(result['category'], result['name'])
        else:
            print(f"No snippets found containing '{query}'.")
        

    def write_json(self,data, filename):
        """Helper function to write json"""
    # pass in json data using top level key ex. snippets
    # write to filename provided
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def clear_screen(self):
        ''' Clears the screen based on OS '''
        name = os.name
        # for windows 
        if name == 'nt':
            _ = os.system('cls')
    
            # for mac and linux(here, os.name is 'posix')
        else:
            _ = os.system('clear')
                    

                
