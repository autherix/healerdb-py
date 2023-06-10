import typer, rich, json
import mod_dbquery
import rich
# from rich import print
from rich.console import Console

# console = Console()
app = typer.Typer(help="Manage the documents", no_args_is_help=True)

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
def list(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to list the documents IDs from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to list the documents IDs from", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """List all the documents IDs"""
    result = mod_dbquery.ListDocuments(client, dbname, colname)

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
def create(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to create the document in", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to create the document in", rich_help_panel="neccessary Information"),
    doc: str = typer.Option(..., "--document", "-doc", help="The json document content as string to create, Use quotes to wrap the entire string and double quotes to wrap the each key and value", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Create a document"""
    result = mod_dbquery.AddDocument(client, dbname, colname, doc)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def delete(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to delete the document from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to delete the document from", rich_help_panel="neccessary Information"),
    docid: str = typer.Option(..., "--document-id", "-docid", help="The document id to delete", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete a document"""
    result = mod_dbquery.RemoveDocument(client, dbname, colname, docid)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def exists(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to check the document in", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to check the document in", rich_help_panel="neccessary Information"),
    docid: str = typer.Option(..., "--document-id", "-docid", help="The document id to check", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Check if a document exists"""
    result = mod_dbquery.IsDocument(client, dbname, colname, docid)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def update_one_by_id(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to update the document in", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to update the document in", rich_help_panel="neccessary Information"),
    docid: str = typer.Option(..., "--document-id", "-docid", help="The document id to update", rich_help_panel="neccessary Information"),
    doc: str = typer.Option(..., "--document", "-doc", help="The new json document content as string to update", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Update a document"""
    result = mod_dbquery.UpdateDocumentByID(client, dbname, colname, docid, doc)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def update_one_by_query(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to update the document in", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to update the document in", rich_help_panel="neccessary Information"),
    query: str = typer.Option(..., "--query", "-q", help="The query to update the document", rich_help_panel="neccessary Information"),
    doc: str = typer.Option(..., "--document", "-doc", help="The new json document content as string to update", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Update a document"""
    result = mod_dbquery.UpdateDocument(client, dbname, colname, query, doc)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)

@app.command(no_args_is_help=True)
def get_one(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to get the document from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to get the document from", rich_help_panel="neccessary Information"),
    query: str = typer.Option(..., "--query", "-q", help="The query to get the document", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Get a document with a query(only one document - first found even if empty query)"""
    result = mod_dbquery.QueryDocument(client, dbname, colname, query)

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
def get_all(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to get the documents from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to get the documents from", rich_help_panel="neccessary Information"),
    query: str = typer.Option(..., "--query", "-q", help="The query to get the documents", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Get documents with a query(empty query for all documents)"""
    result = mod_dbquery.QueryDocuments(client, dbname, colname, query)

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
def update_many_by_query(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to update the documents in", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to update the documents in", rich_help_panel="neccessary Information"),
    query: str = typer.Option(..., "--query", "-q", help="The query to update the documents", rich_help_panel="neccessary Information"),
    doc: str = typer.Option(..., "--document", "-doc", help="The new json document content as string to update", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Update documents with a query"""
    result = mod_dbquery.UpdateDocumentsWithQuery(client, dbname, colname, query, doc)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)




    print(result)

@app.command(no_args_is_help=True)
def delete_all_documents(
    dbname: str = typer.Option(..., "--database", "-db", help="The database to delete the documents from", rich_help_panel="neccessary Information"),
    colname: str = typer.Option(..., "--collection", "-coll", help="The collection to delete the documents from", rich_help_panel="neccessary Information"),
    IsJson: bool = typer.Option(False, "--json", "-j", help="Output in JSON format"),
    ):
    """Delete all documents in a collection"""
    result = mod_dbquery.PurgeDocuments(client, dbname, colname)

    if (IsJson or gIsJson) and type(result) is not dict:
        # Convert the list to a dictionary
        result = { "result": str(result) }
        # Convert the dictionary to a JSON string
        result = json.dumps(result, indent=4)

    print(result)





if __name__ == "__main__":
    app()
