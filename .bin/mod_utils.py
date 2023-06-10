import os, inspect, yaml, sys, json, gjson
# from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.theme import Theme
from rich.emoji import Emoji
from mongoquery import Query, QueryError
from bson import ObjectId

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
    diagMsgStylized = stylize(str(inspect.stack()[1].frame.f_code.co_filename), "bright_black") + ":" + stylize(str(inspect.stack()[1].frame.f_code.co_firstlineno), "bright_black") + " > " + stylize(str(inspect.stack()[1].frame.f_code.co_name), "green_yellow")
    print("▋[purple]diag[/purple] ▋ " + diagMsgStylized)
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
    if type(err) == str:
        newErrorMsg = "[red][b]ERROR: [/b][/red]" + err
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

# function NthKey which gets a dictionary and a number and returns a key-value pair of the nth key in the dictionary
def NthKey(dictionary, n):
    # Get the nth key in the dictionary
    key = list(dictionary.keys())[n]
    # Get the value of the nth key
    value = dictionary[key]
    # convert it to a dictionary and return it
    return {key: value}

# function ShiftLeft which gets a dictionary and a number and returns a dictionary with the keys shifted left by the number provided
def ShiftLeft(dictionary, n=1):
    # Get the keys of the dictionary
    keys = list(dictionary.keys())
    # Get the values of the dictionary
    values = list(dictionary.values())
    # Shift the keys left by n
    newKeys = keys[n:]
    # Shift the values left by n
    newValues = values[n:]
    # Create a new dictionary with the new keys and values
    newDict = dict(zip(newKeys, newValues))
    # Return the new dictionary
    return newDict

# function GetFromJson which gets a json object and some queries and paths ( All would be set as *args ) and returns the value of the query and error
def GetFromJson(jsondoc, *args):
    # rprint("jsondoc before: ")
    # print(jsondoc)
    # Iterate over the args
    for arg in args:
        # seperator()
        # print("arg: " + str(arg))
        # If the arg is not a string, raise an error
        if type(arg) != str:
            return None, Exception("Invalid query provided")
        
        # Try to convert arg to json
        try:
            arg = json.loads(arg)
            # rprint("arg is json")
            # On success, use arg to create the query
            jsonq = Query(arg)
            # Get the value of the query from jsondoc
            jsondoc = list(filter(jsonq.match, jsondoc))
            # If the jsondoc is empty, return None
            if len(jsondoc) == 0:
                return None, None
            # print("jsondoc after: " + str(jsondoc))
            pass
        except Exception as err:
            # rprint("arg is not json")
            # If jsondoc is list
            if type(jsondoc) == list:
                if len(jsondoc) == 1:
                    # Set jsondoc to the first element of the list
                    jsondoc = jsondoc[0]
                    # print("jsondoc first element set: " + str(jsondoc))
            # If current jsondoc is a list, iterate over it and try to get the value of the query
            if type(jsondoc) == list:
                # print("jsondoc is a list")
                # Iterate over the list, append the result of the query on each item to a new list
                newJsondoc = []
                for item in jsondoc:
                    try:
                        # print("current item: " + str(item))
                        # while item is a list, get the first item and save it in item
                        while type(item) == list:
                            item = item[0]
                        item = item[arg]
                        # print("item after: " + str(item))
                        # Append the result to the new list
                        newJsondoc.append(item)
                        # print("whole jsondoc after: " + str(newJsondoc))
                        pass
                    except Exception as err:
                        return None, err
                jsondoc = newJsondoc
                # jsonQuery = Query(arg)
                # jsondoc = list(filter(jsonQuery.match, jsondoc))
                # If the jsondoc is empty, return None
                if len(jsondoc) == 0:
                    # print("jsondoc is empty")
                    return None, None
                # print("jsondoc after: " + str(jsondoc))
                pass

            # If current jsondoc is a dictionary, try to get the value of the query from the current item
            elif type(jsondoc) == dict:
                # print("jsondoc is a dict")
                try:
                    jsondoc = jsondoc[arg]
                    # print("jsondoc after: " + str(jsondoc))
                    pass
                except Exception as err:
                    return None, err
            else:
                return None, err
    return jsondoc, None

def GetFromJson2(jsondoc, path):
    # Use gjson to get the value of the query from jsondoc
    jsondoc = gjson.Get(jsondoc, path)
    # If the jsondoc is empty, return None
    if len(jsondoc) == 0:
        return None, None
    return jsondoc, None

def convert_dict_to_json(data):
    def json_encoder(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    return json.dumps(data, default=json_encoder)