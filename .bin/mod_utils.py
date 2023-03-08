import os, inspect, yaml, sys
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
    seperator(90, sepchr)
    # Print the message
    diagMsgStylized = stylize(str(inspect.stack()[1].frame.f_code.co_filename), "bright_black") + ":" + stylize(str(inspect.stack()[1].frame.f_code.co_firstlineno), "bright_black") + " > " + stylize(str(inspect.stack()[1].frame.f_code.co_name), "green_yellow")
    print("▋[purple]diag[/purple] ▋ " + diagMsgStylized)
    seperator(90, sepchr_up)
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
    if type(err) == str:
        newErrorMsg = "[red][b]ERROR:[/b][/red]" + err
    else:
        print("Error type: " + str(type(err)))
        print("error text: " + str(err))
        # Get all error info from the error object
        errType = type(err).__name__
        errArgs = err.args
        errTraceback = err.__traceback__

        # Get the error message from the error object
        errMessage = str(err)

        # Get the error line number from the error object
        errLineNumber = errTraceback.tb_lineno if errTraceback else "None"

        # Get the error file name from the error object
        errFileName = errTraceback.tb_frame.f_code.co_filename if errTraceback else "None"

        # Get the error function name from the error object
        errFunctionName = errTraceback.tb_frame.f_code.co_name if errTraceback else "None"

        # Get the error line code from the error object
        errLineCode = errTraceback.tb_frame.f_code.co_code if errTraceback else "None"

        newErrorMsg = "[red][b]ERROR:[/b][/red] [b]" + errMessage + "[yellow]\nTraceback:   [yellow]Function: [/yellow][grey58]" + str(errFunctionName) + "[/grey58]\n\tFile: [/yellow][grey66]" + str(errFileName) + ":" + str(errLineNumber) + "[/grey66]"

    return newErrorMsg

# function stylize to stylize a string with rich library
def stylize(text, *args):
    # Iterate over the args and apply the styles
    for arg in args:
        text = "[" + arg + "]" + text + "[/" + arg + "]"
    return text

# function IsPath to check if a file or folder with the provided path exists, return True if the file exists and error 
def IsPath(path, type="file"):
    if type == "file":
        try:
            # Check if the file exists
            if os.path.isfile(path):
                return True, None
            else:
                return False, None
        except Exception as err:
            return None, err
    elif type == "dir" or type == "directory":
        try:
            # Check if the file exists
            if os.path.isdir(path):
                return True, None
            else:
                return False, None
        except Exception as err:
            return None, err
    else:
        # raise a custom exception if the type is not valid and save it in the error variable
        return None, Exception("Invalid type provided")

# function loadYamlConfig to load the config file and return the config and error
def loadYamlConfig(configfile= "/ptv/healer/healerdb-py/.bin/config/config.yaml"):
    # Check if the config file exists
    configExists, err = IsPath(configfile, "file")
    if err:
        return None, err
    if configExists:
        try:
            # Load the config file as yaml
            with open(configfile, 'r') as stream:
                config = yaml.safe_load(stream)
                return config, None
        except Exception as err:
            return None, err
    else:
        return None, Exception("Config file not found")