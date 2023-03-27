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
    global IsJson
    IsJson = OutIsJson



@app.command()
def list(
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the databases"""
    result = mod_dbquery.GetDatabases(client)
    if IsJson:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)    
    
@app.command()
def create(dbname: str):
    """Create a database"""
    result = mod_dbquery.CreateDatabase(client, dbname)
    print(result)


if __name__ == '__main__':
    app()