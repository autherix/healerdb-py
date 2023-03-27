import os, sys, inspect, time, click, json, yaml
from mod_utils import *
import mod_utils as myutils

# function getcfg(path="config/config.yaml") to get the config file from the path, parse it as json or yaml and return config object and error
def getcfg(path="config/config.yaml"):
    # import the config file
    if path.endswith(".yaml") or path.endswith(".yml"):
        with open(path, "r") as f:
            config = yaml.safe_load(f)
    elif path.endswith(".json"):
        with open(path, "r") as f:
            config = json.load(f)
    else:
        return None, Exception("Invalid config file format")
    return config, None

# function GetConfig to get the database config from the config file and return the config and error
def GetConfig(*args):
    # Define config
    config, err = myutils.loadYamlConfig(*args)
    if err != None:
        return None, err
    return config, None

# function GetConnstr to get the connection string from the config file and return the connection string and error
def GetConnstr(*args):
    # Get the config
    config, err = GetConfig(*args)
    if err != None:
        return None, err

    # Get the database config
    dbconfig = config["database"]
    db_base_url = dbconfig["url"]["base_url"]
    db_username = dbconfig["url"]["creds"]["username"]
    db_password = dbconfig["url"]["creds"]["password"]
    db_host = dbconfig["url"]["host"]
    db_port = str(dbconfig["url"]["port"])
    connstr = db_base_url + db_username + ":" + db_password + "@" + db_host + ":" + db_port + "/"

    return connstr, None
