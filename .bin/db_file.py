import typer, rich, json
import mod_dbquery
import rich
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the Files", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the file command"""
    global client
    client = mod_dbquery.FastClient()
    global gIsJson
    gIsJson = OutIsJson

@app.command(no_args_is_help=True)
def list(
    database: str = typer.Option(..., "--database", "-db", help="The database to list the files in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to list the files in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to list the files in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to list the files in", rich_help_panel="neccessary Information"),
    directory: str = typer.Option(..., "--directory", "-dir", help="The directory to list the files in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the files"""
    result = mod_dbquery.ListFiles(client, database, target, domain, subdomain, directory)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def exists(
    database: str = typer.Option(..., "--database", "-db", help="The database to check the file in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to check the file in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to check the file in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to check the file in", rich_help_panel="neccessary Information"),
    directory: str = typer.Option(..., "--directory", "-dir", help="The directory to check the file in", rich_help_panel="neccessary Information"),
    file: str = typer.Option(..., "--file", "-f", help="The file to check", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a file exists"""
    result = mod_dbquery.IsFile(client, database, target, domain, subdomain, directory, file)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def multi_create(
    database: str = typer.Option(..., "--database", "-db", help="The database to create the files in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to create the files in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to create the files in", rich_help_panel="neccessary Information"),
    directory: str = typer.Option(..., "--directory", "-dir", help="The directory to create the files in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to create the files in", rich_help_panel="neccessary Information"),
    file: str = typer.Option(..., "--file", "-f", help="The file to create", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create multiple files"""
    result = mod_dbquery.AddFiles(client, database, target, domain, subdomain, directory, file)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete(
    database: str = typer.Option(..., "--database", "-db", help="The database to delete the file in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to delete the file in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to delete the file in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to delete the file in", rich_help_panel="neccessary Information"),
    directory: str = typer.Option(..., "--directory", "-dir", help="The directory to delete the file in", rich_help_panel="neccessary Information"),
    file: str = typer.Option(..., "--file", "-f", help="The file to delete", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a file"""
    result = mod_dbquery.RemoveFile(client, database, target, domain, subdomain, directory, file)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)




if __name__ == "__main__":
    app()