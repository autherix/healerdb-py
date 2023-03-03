import os, inspect
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

# function ErrGen to generate a complete error message to be printed with the rich library and more helpful data
def ierr(err, inspectFrame):
    fullstack = inspect.stack()
    caller = "Caller Module:", str(fullstack[1][1]) + ":" + str(fullstack[1][2]) + " > Function: " + str(fullstack[1].frame.f_code.co_name)
    newError = "------------------------\n" + "[red]ERR[/red] > " + str(inspectFrame.f_code.co_filename) + ":"+str(inspectFrame.f_code.co_firstlineno) + " > " + str(inspectFrame.f_code.co_name) + " :\n > " + str(err) + "\nCaller Info:\n" + str(caller) + "\n------------------------"
    return newError

# function rprint to print a message with rich library, with a starter template for telling which file and function is printing the message
def rprint(msg="", *args):
    # if msg is an array, convert it to a string with delimiter " "
    if type(msg) == list:
        msg = " ".join(msg)
    # if we have args, convert them to a string with delimiter " "
    if args:
        # iterate over args and convert them to string and append them to the end of msg
        for arg in args:
            msg = msg + " " + str(arg)
    # Print the message
    print("[blue]MSG[/blue] > " + extractFileName(str(inspect.stack()[1].frame.f_code.co_filename)) + ":"+str(inspect.stack()[1].frame.f_code.co_firstlineno) + " > " + str(inspect.stack()[1].frame.f_code.co_name) + " :\n > " + str(msg))
    seperator(60, "-")
    return

# function extractFileName to extract the filename from a path
def extractFileName(path):
    # split the path by the "/" character
    path = path.split("/")
    # return the last element of the list
    return path[-1]