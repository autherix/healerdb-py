import typer, rich, json
import mod_dbquery
import rich
from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the databases", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the database command"""
    global client
    client = mod_dbquery.FastClient()
    global gIsJson
    gIsJson = OutIsJson



@app.command(no_args_is_help=False)
def list(
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the databases"""
    result = mod_dbquery.GetDatabases(client)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)
    
@app.command(no_args_is_help=True)
def create(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to create", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create a database"""
    result = mod_dbquery.CreateDatabase(client, dbname)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to delete", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a database"""
    result = mod_dbquery.DropDatabase(client, dbname)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def exists(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to check if it exists", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a database exists"""
    result = mod_dbquery.IsDatabase(client, dbname)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def purge_all_databases(
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete all databases"""
    result = mod_dbquery.PurgeDatabases(client)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

if __name__ == '__main__':
    app()