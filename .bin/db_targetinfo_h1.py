import typer, rich, json
import mod_dbquery
import rich
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the Targets Information in Hackerone platforms", no_args_is_help=True)

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
    """Check if a HackerOne target exists in the database"""
    result = mod_dbquery.IsTargetInfo_h1(client, dbname, colname, target_handle)

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
    doc: str = typer.Option(..., "--document", "-doc", help="The document to insert", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create/Update a HackerOne target in the database"""
    result = mod_dbquery.AddTargetInfo_h1(client, dbname, colname, doc)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

