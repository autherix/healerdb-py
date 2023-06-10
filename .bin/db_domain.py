import typer, rich, json
import mod_dbquery
import rich
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the domains", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the domain command"""
    global client
    client = mod_dbquery.FastClient()
    global gIsJson
    gIsJson = OutIsJson



@app.command(no_args_is_help=True)
def list(
    database: str = typer.Option(..., "--database", "-db", help="The database to list the domains from", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to list the domains from", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the domains"""
    result = mod_dbquery.ListDomains(client, database, target)[1]

    # if (Isjson or gIsJson) And type of result is not dict:
    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)
    elif type(result) is dict:
        # load as bson
        result = convert_dict_to_json(result)

    print(result)

@app.command(no_args_is_help=True)
def create(
    database: str = typer.Option(..., "--database", "-db", help="The database to create the domain in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to create the domain in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to create", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create a domain"""
    result = mod_dbquery.AddDomain(client, database, target, domain)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete(
    database: str = typer.Option(..., "--database", "-db", help="The database to delete the domain from", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to delete the domain from", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to delete", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a domain"""
    result = mod_dbquery.RemoveDomain(client, database, target, domain)
    if result != "":
        result = result[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def exists(
    database: str = typer.Option(..., "--database", "-db", help="The database to check the domain in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to check the domain in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to check", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a domain exists"""
    result = mod_dbquery.IsDomain(client, database, target, domain)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def get(
    database: str = typer.Option(..., "--database", "-db", help="The database to get the domain from", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to get the domain from", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to get", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Get a domain"""
    result = mod_dbquery.GetDomain(client, database, target, domain)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)
    elif type(result) is dict:
        # load as bson
        result = convert_dict_to_json(result)

    print(result)

@app.command(no_args_is_help=True)
def recreate(
    database: str = typer.Option(..., "--database", "-db", help="The database to init the domain in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to init the domain in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to init", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Init a domain - This will create a domain if does not exist, if exists, removes it and creates it again with a new ID"""
    
    result = mod_dbquery.InitDomain(client, database, target, domain)[1]
    

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete_all_domains(
    database: str = typer.Option(..., "--database", "-db", help="The database to delete all domains from", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to delete all domains from", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete all domains"""
    result = mod_dbquery.PurgeDomains(client, database, target)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)




if __name__ == "__main__":
    app()