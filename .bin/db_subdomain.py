import typer, rich, json
import mod_dbquery
import rich
from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the  subdomains", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the subdomain command"""
    global client
    client = mod_dbquery.FastClient()
    global gIsJson
    gIsJson = OutIsJson

@app.command(no_args_is_help=True)
def list(
    database: str = typer.Option(..., "--database", "-db", help="The database to list the subdomains in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to list the subdomains in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to list the subdomains in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the subdomains"""
    result = mod_dbquery.ListSubdomains(client, database, target, domain)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def create(
    database: str = typer.Option(..., "--database", "-db", help="The database to create the subdomain in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to create the subdomain in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to create the subdomain in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to create", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create a subdomain"""
    result = mod_dbquery.AddSubdomain(client, database, target, domain, subdomain)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete(
    database: str = typer.Option(..., "--database", "-db", help="The database to delete the subdomain from", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to delete the subdomain from", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to delete the subdomain from", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to delete", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a subdomain"""
    result = mod_dbquery.RemoveSubdomain(client, database, target, domain, subdomain)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def exists(
    database: str = typer.Option(..., "--database", "-db", help="The database to check the subdomain in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to check the subdomain in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to check the subdomain in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to check", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a subdomain exists"""
    result = mod_dbquery.IsSubdomain(client, database, target, domain, subdomain)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)



    print(result)





if __name__ == "__main__":
    app()