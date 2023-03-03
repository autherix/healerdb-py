import os, inspect
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.emoji import Emoji

sepchr = "▂"
sepchr_up = "▔"

# Configure rich
console = Console()

# Function to print a seperator
def seperator(size=80, char="-"):
    print(char * size)

# Function to clear the terminal screen
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function logo to print the logo 
def mdview(text):
    pre_md = Emoji.replace(text)
    md = Markdown(pre_md)
    console.print(md)

# function rprint to print a message with rich library, with a starter template for telling which file and function is printing the message
def rprint(msg):
    seperator(80, sepchr)
    # Print the message
    diagMsg = "[bright_black]" + str(inspect.stack()[1].frame.f_code.co_filename) + ":" + str(inspect.stack()[1].frame.f_code.co_firstlineno) + "[/bright_black] > [green_yellow]" + str(inspect.stack()[1].frame.f_code.co_name + "[/green_yellow]")
    print("▋[purple]diag[/purple] > " + diagMsg)
    seperator(80, sepchr_up)
    print("[blue][b]LOG[/b][/blue] > " + str(msg))
    return

# function extractFileName to extract the filename from a path
def extractFileName(path):
    # split the path by the "/" character
    path = path.split("/")
    # return the last element of the list
    return path[-1]

# function parseError to parse the error object and return a string with a complete error message
def parseError(err):
    # Get all error info from the error object
    errType = type(err).__name__
    errArgs = err.args
    errTraceback = err.__traceback__

    # Get the error message from the error object
    errMessage = str(err)

    # Get the error line number from the error object
    errLineNumber = errTraceback.tb_lineno

    # Get the error file name from the error object
    errFileName = errTraceback.tb_frame.f_code.co_filename

    # Get the error function name from the error object
    errFunctionName = errTraceback.tb_frame.f_code.co_name

    # Get the error line code from the error object
    errLineCode = errTraceback.tb_frame.f_code.co_code

    newErrorMsg = "[red][b]ERROR:[/b][/red] [b]" + errMessage + "[yellow]\nTraceback:   [yellow]Function: [/yellow][grey58]" + str(errFunctionName) + "[/grey58]\n\tFile: [/yellow][grey66]" + str(errFileName) + ":" + str(errLineNumber) + "[/grey66]"

    return newErrorMsg

# function stylize to stylize a string with rich library
def stylize(text, *args):
    # Iterate over the args and apply the styles
    for arg in args:
        text = "[" + arg + "]" + text + "[/" + arg + "]"
    return text

