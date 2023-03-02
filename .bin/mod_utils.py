import os
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.emoji import Emoji

# Configure rich
console = Console()

# Function to print a seperator
def seperator(size=60, char="-"):
    print(char * size)

# Function to clear the terminal screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function logo to print the logo 
def mdview(text):
    pre_md = Emoji.replace(text)
    md = Markdown(pre_md)
    console.print(md)