import typer, rich, json
import mod_dbquery
import rich
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the databases", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the target command"""
    global client
    client = mod_dbquery.FastClient()
    global gIsJson
    gIsJson = OutIsJson

@app.command(no_args_is_help=True)
def list(
    database: str = typer.Option(..., "--database", "-db", help="The database to list the targets(collections) in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the targets"""
    result = mod_dbquery.GetCollections(client, database)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def create(
    target: str = typer.Option(..., "--target", "-t", help="The target handle (Must be target's handle in bb platfoem) to create", rich_help_panel="neccessary Information"),
    database: str = typer.Option(..., "--database", "-db", help="The database to create the target in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create a database"""
    result = mod_dbquery.CreateCollection(client, database, target)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete(
    target: str = typer.Option(..., "--target", "-t", help="The target handle (Must be target's handle in bb platfoem) to delete", rich_help_panel="neccessary Information"),
    database: str = typer.Option(..., "--database", "-db", help="The database to delete the target in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a database"""
    result = mod_dbquery.DropCollection(client, database, target)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def exists(
    target: str = typer.Option(..., "--target", "-t", help="The target handle (Must be target's handle in bb platfoem) to check", rich_help_panel="neccessary Information"),
    database: str = typer.Option(..., "--database", "-db", help="The database to check the target in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a target exists"""
    result = mod_dbquery.IsCollection(client, database, target)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete_all_targets(
    database: str = typer.Option(..., "--database", "-db", help="The database to delete all the targets in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete all the targets(collections) in a database"""
    result = mod_dbquery.DropAllCollections(client, database)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)




if __name__ == '__main__':
    app()