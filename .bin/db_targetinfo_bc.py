import typer, rich, json
import mod_dbquery
import rich
from mod_utils import *
from bson import ObjectId
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the Targets Information in BugCrowd platform", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the document command"""
    global client
    client = mod_dbquery.FastClient()
    global gIsJson
    gIsJson = OutIsJson



@app.command(no_args_is_help=True)
def exists(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to list the documents IDs from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to list the documents IDs from", rich_help_panel="neccessary Information"),
    target_handle: str = typer.Option(..., "--handle", help="The handle of the target", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a bugcrowd target exists in the database"""
    result = mod_dbquery.IsTargetInfo_bc(client, dbname, colname, target_handle)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def create(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to list the documents IDs from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to list the documents IDs from", rich_help_panel="neccessary Information"),
    doc: str = typer.Option(..., "--document", "-doc", help="The document file address to insert its contents", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create/Update a bugcrowd target in the database"""
    result = mod_dbquery.AddTargetInfo_bc(client, dbname, colname, doc)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def list(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to list the documents IDs from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to list the documents IDs from", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List the documents handles in a collection"""
    result = mod_dbquery.ListTargetInfo_bc(client, dbname, colname)

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
def get(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to list the documents IDs from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to list the documents IDs from", rich_help_panel="neccessary Information"),
    target_handle: str = typer.Option(..., "--handle", help="The handle of the target", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Get a bugcrowd target from the database"""
    result = mod_dbquery.GetTargetInfo_bc(client, dbname, colname, target_handle)

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
def delete(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to list the documents IDs from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to list the documents IDs from", rich_help_panel="neccessary Information"),
    target_handle: str = typer.Option(..., "--handle", help="The handle of the target", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a bugcrowd target from the database"""
    result = mod_dbquery.RemoveTargetInfo_bc(client, dbname, colname, target_handle)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)




if __name__ == "__main__":
    app()