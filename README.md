
# pysnippet

A lightweight CLI-based code snippet manager that helps you organize, retrieve, and reuse your code snippets. There
are many like this but I wanted one that would have just a menu and allow you to be in a specific context. If you
choose snippets from the main menu then it can put you in a specific category and the prompt reflects it eg. docker#
Then all snippets accessed are in that category.

## Features

- Interactive menu-based interface with intuitive navigation
- Smart autocompletion powered by Python's prompt_toolkit
- Comprehensive snippet management:
  - Create, view, update, and delete snippets
  - Organize snippets in custom categories
  - Search across all snippets
- Clipboard integration for quick copy-paste workflow (Tested on Mac and Linux only)
- Editor integration to create and modify snippets in your preferred editor

## Installation


### From Source

```bash
git clone https://github.com/Philip741/pysnippet.git
cd pysnippet
pip install .
```
If you use a virtual environment make sure it is created and
sourced outside the pysnippet source directory.

### From Wheel
This is currently recommended.

Download the latest wheel file from the releases page and install:

```bash
pip install pysnippet-0.1.0-py3-none-any.whl
```
You can also choose to create a virtual environment then install in there.

## Usage

Once install run the following command:

```bash
pysnippet
```
Pressing tab will display options with autocomplete

### Commands

- `help` - Display available commands
- `snippets` - Browse and access your snippets
- `add-category` - Create a new snippet category
- `search` - Search through all your snippets
- `snippet-categories` - List all available categories
- `exit` - Exit the program

## Configuration

pysnippet stores its configuration in `~/.pysnippet/pysnip.cfg` and snippets in `~/.snippets/`.

## Requirements

- Python 3.6+
- prompt_toolkit
- pyperclip (optional, for clipboard support)

May need something like xclip if your Linux distro has no clipboard functionality pyperclip can find.

## License

MIT

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
