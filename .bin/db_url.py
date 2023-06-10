import typer, rich, json
import mod_dbquery
import rich
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the urls", no_args_is_help=True)

@app.callback()
def callback(
    OutIsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Callback function for the url command"""
    global client
    client = mod_dbquery.FastClient()
    global gIsJson
    gIsJson = OutIsJson

@app.command(no_args_is_help=True)
def list(
    database: str = typer.Option(..., "--database", "-db", help="The database to list the URLs in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to list the URLs in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to list the URLs in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to list the URLs in", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the URLs inside a domain"""
    result = mod_dbquery.ListUrls(client, database, target, domain, subdomain)[1]

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)
    
    print(result)

@app.command(no_args_is_help=True)
def exists(
    database: str = typer.Option(..., "--database", "-db", help="The database to check the URL in", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to check the URL in", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to check the URL in", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to check the URL in", rich_help_panel="neccessary Information"),
    url: str = typer.Option(..., "--url", "-u", help="The URL to check", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a URL exists"""
    result = mod_dbquery.IsUrl(client, database, target, domain, subdomain, url)[1]
    
    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def multi_create(
    database: str = typer.Option(..., "--database", "-db", help="The database to add the URLs to", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to add the URLs to", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to add the URLs to", 
    rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to add the URLs to"),
    urls: str = typer.Option(..., "--urls", "-u", help="The URLs to add",
    rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Add multiple URLs to a domain"""
    result = mod_dbquery.AddUrls(client, database, target, domain, subdomain, urls)

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
    database: str = typer.Option(..., "--database", "-db", help="The database to delete the URL from", rich_help_panel="neccessary Information"),
    target: str = typer.Option(..., "--target", "-t", help="The target to delete the URL from", rich_help_panel="neccessary Information"),
    domain: str = typer.Option(..., "--domain", "-d", help="The domain to delete the URL from", rich_help_panel="neccessary Information"),
    subdomain: str = typer.Option(..., "--subdomain", "-sub", help="The subdomain to delete the URL from", rich_help_panel="neccessary Information"),
    url: str = typer.Option(..., "--url", "-u", help="The URL to delete", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a URL from a domain"""
    result = mod_dbquery.RemoveUrl(client, database, target, domain, subdomain, url)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": result }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)
    elif type(result) is dict:
        # load as bson
        result = convert_dict_to_json(result)

    print(result)








if __name__ == '__main__':
    app()