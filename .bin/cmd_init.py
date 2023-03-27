import os, typer
import mod_dbquery as dbquery
from mod_utils import *
import mod_config

def initdb(client):

    # Purge the database
    purgeResult, err = dbquery.PurgeDatabases(client)
    if err != None:
        print(parseError(err))
    rprint("Purge result: " + str(purgeResult))

    # Create a database called enum
    db, err = dbquery.CreateDatabase(client, "enum")
    if err != None:
        print(parseError(err))
    rprint("Database created successfully")
    seperator()

    # Create a collection called target1
    collection, err = dbquery.CreateCollection(client, "enum", "target1")
    if err != None:
        print(parseError(err))
    rprint("Collection created successfully")
    seperator()

    # Create a domain object called domain1.com
    domain1, err = dbquery.AddDomain(client, "enum", "target1", "domain1.com")
    if err != None:
        print(parseError(err))
    rprint("Domain created successfully")

    # list domains in the collection target1
    docs, domainList, err = dbquery.ListDomains(client, "enum", "target1")
    if err != None:
        print(parseError(err))
    rprint("Domains in collection target1: " + str(domainList))

    # List the subdomains of domain1.com in the collection target1
    docs, subdomainList, err = dbquery.ListSubdomains(client, "enum", "target1", "domain1.com")
    if err != None:
        print(parseError(err))
    rprint("Subdomains of domain1.com in collection target1: " + str(subdomainList))

    # Add a new subdomain to domain1.com in the collection target1
    subdomain1, doc_id,  err = dbquery.AddSubdomain(client, "enum", "target1", "domain1.com", "subdomain1")
    if err != None:
        print(parseError(err))
    rprint("Subdomain created successfully: " + stylize(str(subdomain1), "blue"))

    # List the subdomains of domain1.com in the collection target1
    docs, subdomainList, err = dbquery.ListSubdomains(client, "enum", "target1", "domain1.com")
    if err != None:
        print(parseError(err))
    rprint("Subdomains of domain1.com in collection target1: " + str(subdomainList))

    # Add a new subdomain to domain1.com in the collection target1
    subdomain2, doc_id, err = dbquery.AddSubdomain(client, "enum", "target1", "domain1.com", "subdomain2")
    if err != None:
        print(parseError(err))
    rprint("Subdomain created successfully: " + stylize(str(subdomain2), "blue"))

    # List the subdomains of domain1.com in the collection target1
    docs, subdomainList, err = dbquery.ListSubdomains(client, "enum", "target1", "domain1.com")
    if err != None:
        print(parseError(err))
    rprint("Subdomains of domain1.com in collection target1: " + str(subdomainList))

    # Remove subdomain subdomain1 from domain1.com in the collection target1
    doc, doc_id, err = dbquery.RemoveSubdomain(client, "enum", "target1", "domain1.com", "subdomain1")
    if err != None:
        print(parseError(err))
    rprint("Subdomain removed successfully: " + stylize(str(doc['subdomain']), "blue"))

    # List nested subdomains of subdomain2 in domain1.com in the collection target1
    docs, subdomainList, err = dbquery.ListNestedSubdomains(client, "enum", "target1", "domain1.com", "subdomain2")
    if err != None:
        print(parseError(err))
    rprint("Nested subdomains of subdomain2 in domain1.com in collection target1: " + str(subdomainList))

    # Add a new nested subdomain to subdomain2 in domain1.com in the collection target1
    subdomain3, doc_id, err = dbquery.AddNestedSubdomain(client, "enum", "target1", "domain1.com", "subdomain2", "subdomain3")
    if err != None:
        print(parseError(err))
    rprint("Nested subdomain created successfully: " + stylize(str(subdomain3), "blue"))

    # Run GetInfo function 
    docs, err = dbquery.GetInfo(client, "enum", "target1", '{"domain": "domain1.com"}', "subdomains", '{"subdomain": "subdomain2"}', 'subdomains')
    if err != None:
        print(parseError(err))
    rprint("ListPart result: " + str(docs))
    # if docs is a list, try to convert it to a dictionary
    seperator()

app = typer.Typer()

@app.command()
def init():
    pass

@app.callback(invoke_without_command=True)
def init():
    client = dbquery.FastClient()
    initdb(client)
    print("Done")





if __name__ == "__main__":
    app()