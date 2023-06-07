import typer, rich, json
import mod_dbquery
import rich
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the Parameters", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the parameter command"""
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
    url: str = typer.Option(..., "--url", "-u", help="The url to list the files in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the parameters for a file"""

    result = mod_dbquery.ListUrlParameters(client, database, target, domain, subdomain, url)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def multi_create(
    database: str = typer.Option(..., "--database", "-db", help="The database to create the files in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to create the files in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to create the files in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to create the files in", rich_help_panel="neccessary Information"),
    url: str = typer.Option(..., "--url", "-u", help="The url to create the files in", rich_help_panel="neccessary Information"),
    parameters: str = typer.Option(..., "--parameter", "-p", help="The parameters to create", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create multiple parameters"""

    result = mod_dbquery.AddUrlParameters(client, database, target, domain, subdomain, url, parameters)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def exists(
    database: str = typer.Option(..., "--database", "-db", help="The database to check the parameters in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to check the parameters in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to check the parameters in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to check the parameters in", rich_help_panel="neccessary Information"),
    url: str = typer.Option(..., "--url", "-u", help="The url to check the parameters in", rich_help_panel="neccessary Information"),
    parameter: str = typer.Option(..., "--parameter", "-p", help="The parameter to check", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a parameter exists"""

    result = mod_dbquery.IsUrlParameter(client, database, target, domain, subdomain, url, parameter)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete(
    database: str = typer.Option(..., "--database", "-db", help="The database to delete the parameters in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to delete the parameters in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to delete the parameters in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to delete the parameters in", rich_help_panel="neccessary Information"),
    url: str = typer.Option(..., "--url", "-u", help="The url to delete the parameters in", rich_help_panel="neccessary Information"),
    parameter: str = typer.Option(..., "--parameter", "-p", help="The parameter to delete", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a parameter"""

    result = mod_dbquery.RemoveUrlParameter(client, database, target, domain, subdomain, url, parameter)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)


if __name__ == "__main__":
    app()