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



@app.command()
def list(
    database: str = typer.Option(..., "--database", "-db", help="The database to list the collections in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the databases"""
    result = mod_dbquery.GetCollections(client, database)

    if IsJson or gIsJson:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command()
def create(
    collection: str = typer.Option(..., "--collection", "-coll", help="The collection to create", rich_help_panel="neccessary Information"),
    database: str = typer.Option(..., "--database", "-db", help="The database to create the collection in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create a database"""
    result = mod_dbquery.CreateCollection(client, database, collection)

    if IsJson or gIsJson:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command()
def delete(
    collection: str = typer.Option(..., "--collection", "-coll", help="The collection to delete", rich_help_panel="neccessary Information"),
    database: str = typer.Option(..., "--database", "-db", help="The database to delete the collection in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a database"""
    result = mod_dbquery.DropCollection(client, database, collection)

    if IsJson or gIsJson:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)
    
    print(result)




if __name__ == '__main__':
    app()