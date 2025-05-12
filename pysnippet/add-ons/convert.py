import os
import json
import sys

def convert_item(file_path, category,name, snippets_path="~/.snippets", append=True):
    """Convert existing text to json useable by pysnippet

       Args:
           file_path (str):
           category (str):
           name (str):
           append(bool):
    """
    # expand user needed to expand the ~ to home path
    snippets_path = os.path.expanduser(snippets_path)
    json_path = os.path.join(snippets_path, f"{category}.json")
    print(json_path)
    print(os.path.exists(json_path))

    with open(file_path, 'r') as f:
        file_lines = [line for line in f]

    if append and os.path.exists(json_path):
        try:
            # open text file to convert
                
                with open(json_path, 'r') as f:
                    data = json.load(f)

                    # update the data
                    data[name] = file_lines
           
        except Exception as e:
            print(f"Error converting item: {e}")
            return False
    # create new category and append text to convert to json file
    else:
        print("hit else in convert_item")
        data = {name: file_lines}

    write_json(data, json_path)
    return True

def write_json(data, filename):
    """Helper function to write json"""
# pass in json data using top level key ex. snippets
# write to filename provided
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def batch_convert(source_dir, category,snippets_path,file_pattern="*.md"):
    """Convert multiple text files in a directory to snippets.
    
    Args:
        source_dir (str): Directory containing text files
        category (str): Category to save snippets under
        snippets_path (str): Path to snippets directory
        file_pattern (str): Pattern to match files
        
    Returns:
        int: Number of files successfully converted
    """
    import glob
    
    success_count = 0
    file_paths = glob.glob(os.path.join(source_dir, file_pattern))
    
    for file_path in file_paths:
        # Use the filename without extension as the snippet name
        name = os.path.splitext(os.path.basename(file_path))[0]
        if convert_item(file_path, category, name, snippets_path):
            success_count += 1
    
    return success_count

def print_usage():
    """Print usage instructions."""
    print("Usage:")
    print("  1. Convert a single file:")
    print("     python convert.py 1 file_path category snippet_name [snippets_path] [append]")
    print("  2. Batch convert files in a directory:")
    print("     python convert.py 2 source_dir category [snippets_path] [file_pattern]")
    print("     - append: 'yes' to append (default), 'no' to create new")
    print("\nExamples:")
    print("  python convert.py 1 ~/code/script.py python my_script")
    print("  python convert.py 1 ~/code/script.py python my_script ~/.snippets no")
    print("  python convert.py 2 ~/code/python_scripts python ~/.snippets *.py")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "1":
        # Single file conversion
        if len(sys.argv) < 5:
            print("Error: Not enough arguments for single file conversion")
            print_usage()
            sys.exit(1)
            
        file_path = sys.argv[2]
        category = sys.argv[3]
        name = sys.argv[4]
        snippets_path = sys.argv[5] if len(sys.argv) > 5 else "~/.snippets"

        # Check if append flag is specified
        append = True
        if len(sys.argv) > 6:
            # if user inputs no it would be equal to no but checking != makes it false
            append = sys.argv[6].lower() != "no"
        
        convert_item(file_path, category, name, snippets_path, append)
    
    elif mode == "2":
        # Batch conversion
        source_dir = sys.argv[2]
        category = sys.argv[3]
        snippets_path = sys.argv[4] if len(sys.argv) > 4 else "~/.snippets"
        file_pattern = sys.argv[5] if len(sys.argv) > 5 else "*.txt"
        
        batch_convert(source_dir, category, snippets_path, file_pattern)
    
    else:
        print(f"Unknown mode: {mode}")
        print_usage()
        sys.exit(1)
