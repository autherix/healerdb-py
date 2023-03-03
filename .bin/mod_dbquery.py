import inspect
from pymongo import MongoClient
from rich import print
from mod_utils import *
# function CreateClient to create a client on mongodb server using the provided connection string, return client and error if any
def CreateClient(connstr):
    try:
        client = MongoClient(connstr)
        rprint("[+] Client Created")
        return client, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function DisconnectClient to disconnect the client from mongodb server
def DisconnectClient(client):
    client.close()
    rprint("[+] Client Disconnected")
    return

# function PingClient to ping the client to the mongodb server, returns a boolean and an error
def PingClient(client):
    try:
        return client.admin.command('ping'), None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function GetDatabases to get client and return list of databases names and error if any
def GetDatabases(client):
    try:
        rprint("[] get database names")
        return client.list_database_names(), None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function CheckDatabase to check if a database with the given name exists, returns a boolean and an error
def CheckDatabase(client, dbname):
    try:
        rprint("[] check if database exists")
        return dbname in client.list_database_names(), None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function PurgeDatabases to delete all the databases in the database except the admin and config databases, returns an error
def PurgeDatabases(client):
    try:
        for db in client.list_database_names():
            if db not in ["admin", "config", "local"]:
                client.drop_database(db)
        rprint("[+] Databases Purged")
        return None
    except Exception as err:
        return ierr(err, inspect.currentframe())

# function CheckCollection to check if a collection with the given name exists in the given database, returns a boolean and an error
def CheckCollection(client, dbname, collname):
    try:
        rprint("[] check if collection [green]{}[/green] exists".format(collname))
        return collname in client[dbname].list_collection_names(), None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function CheckDocument to check if a document with the given id exists in the given collection in the given database, returns a boolean and an error
def CheckDocument(client, dbname, collname, docid):
    try:
        rprint("[] check if document [green]{}[/green] exists in collection [green]{}[/green] in database {}".format(docid, collname, dbname))
        return client[dbname][collname].find_one({"_id": docid}) != None, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function CreateDocument to create a document in the given collection in the given database, with the provided json string of the document, returns the _id of the created document and an error
def CreateDocument(client, dbname, collname, doc):
    try:
        rprint("[] create document in collection [green]{}[/green] in database {}".format(collname, dbname))
        return client[dbname][collname].insert_one(doc).inserted_id, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function CreateCollection to create a collection, with the provided name, in the given database, returns collection name and error 
def CreateCollection(client, dbname, collname):
    try:
        rprint("[] create collection [green]{}[/green] in database {}".format(collname, dbname))
        return client[dbname].create_collection(collname).name, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function CreateDatabase to create a database, with the provided name, returns an error -> for creating a database, it just creates a collection in the database with the name 'exists' and the content as 'exists': true
def CreateDatabase(client, dbname):
    try:
        rprint("[] create database {}".format(dbname))
        return CreateCollection(client, dbname, "exists")
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function DropCollection to drop a collection, with the provided name(removes if exists), in the given database, returns an error
def DropCollection(client, dbname, collname):
    try:
        rprint("[] drop collection [green]{}[/green] in database {}".format(collname, dbname))
        client[dbname].drop_collection(collname)
        return None
    except Exception as err:
        return ierr(err, inspect.currentframe())

# function DropDatabase to drop a database, with the provided database name(removes database if exists), returns an error
def DropDatabase(client, dbname):
    try:
        rprint("[] drop database {}".format(dbname))
        client.drop_database(dbname)
        return None
    except Exception as err:
        return ierr(err, inspect.currentframe())

# function GetCollections to get the the client to the database, a database name, fetches all collection names in the given database and returns an array containing the names of the collections and an error
def GetCollections(client, dbname):
    try:
        rprint("[] get collection names in database {}".format(dbname))
        return client[dbname].list_collection_names(), None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function GetDocuments to get the the client to the database, a database name and a collection name, fetches all documents in the given collection, converts each document to a string of json object and returns an array containing the json objects and an error
def GetDocuments(client, dbname, collname):
    try:
        rprint("[] get documents in collection [green]{}[/green] in database {}".format(collname, dbname))
        docs = []
        for doc in client[dbname][collname].find():
            docs.append(doc)
        return docs, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function GetDocument to get client to database, database name, collection name and document id, fetches the document with the given id from the given collection in the given database, converts the document to a string of json object and returns the json object and an error
def GetDocument(client, dbname, collname, docid):
    try:
        rprint("[] get document [green]{}[/green] in collection [green]{}[/green] in database {}".format(docid, collname, dbname))
        return client[dbname][collname].find_one({"_id": docid}), None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function CountDocuments to get 

# function DeleteDocument to get client to database, database name, collection name and document id, deletes the document with the given id from the given collection in the given database, returns an error
def DeleteDocument(client, dbname, collname, docid):
    try:
        rprint("[] delete document [green]{}[/green] in collection [green]{}[/green] in database [green]{}[/green] with document ID {}".format(docid, collname, dbname))
        client[dbname][collname].delete_one({"_id": docid})
        return None
    except Exception as err:
        return ierr(err, inspect.currentframe())

# function InsertDocument to get client, db, coll, and json document, inserts the document into the collection, returns an error
def InsertDocument(client, dbname, collname, doc):
    try:
        rprint("[] insert document in collection [green]{}[/green] in database {}".format(collname, dbname))
        client[dbname][collname].insert_one(doc)
        return None
    except Exception as err:
        return err  

# function InsertDocuments to get client, db, coll, document id and document string, inserts the documents into the collection in the database, returns an array containing the _id of the added documents and an error
def InsertDocuments(client, dbname, collname, docs):
    try:
        rprint("[] insert documents in collection [green]{}[/green] in database {}".format(collname, dbname))
        return client[dbname][collname].insert_many(docs).inserted_ids, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function AddUniqueIndex to add unique index to a collection in a database, returns an error
def AddUniqueIndex(client, dbname, collname, index):
    try:
        rprint("[] add unique index to collection [green]{}[/green] in database {}".format(collname, dbname))
        client[dbname][collname].create_index(index, unique=True)
        return None
    except Exception as err:
        return ierr(err, inspect.currentframe())

# function CheckTarget to check if a collection exists in the database, returns a boolean and an error
def CheckTarget(client, dbname, target):
    try: 
        rprint("[] check if target [green]{}[/green] exists in database {}".format(target, dbname))
        # Query the database for the collection, use CheckCollection() to check if a collection exists
        return CheckCollection(client, dbname, target)
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function AddTarget to add a collection to the database, returns an error
def AddTarget(client, dbname, target):
    rprint("[] add target [green]{}[/green] to database {}".format(target, dbname))
    try:
        # Check if the target already exists
        exists, err = CheckTarget(client, dbname, target)
        if err != None:
            return ierr(err, inspect.currentframe())
        # If the target already exists, return an error 
        if exists:
            return "Target already exists"
        
        # Add a collection with target name to the database, use CreateCollection() to create a collection
        _, err = CreateCollection(client, dbname, target)
        if err != None:
            return "Error adding target: %s" % ierr(err, inspect.currentframe())
        rprint("Added target: %s" % target)
        return None
    except Exception as err:
        return ierr(err, inspect.currentframe())

# function QueryDocuments to query the database, parameters are database name, collection name, query object, returns a json objects and an error
def QueryDocuments(client, dbname, collname, query):
    rprint("[] query documents in collection [green]{}[/green] in database {}".format(collname, dbname))
    try:
        # Query the database for the documents, use GetDocuments() to get all documents in a collection
        docs, err = GetDocuments(client, dbname, collname)
        if err != None:
            return None, ierr(err, inspect.currentframe())
        # If no documents are found, return an error
        if len(docs) == 0:
            return "", None
        
        # Query the documents for the given query object
        results = []
        for doc in docs:
            if all(item in doc.items() for item in query.items()):
                results.append(doc)
        return results, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function UpdateOneDocument  to update a document in the database, returns ID of successfully updated document and an error -> get client, db, collection name, document id, object(as json) in parameters
def UpdateOneDocument(client, dbname, collname, docid, jsonobj):
    try:
        rprint("[] update document [green]{}[/green] in collection [green]{}[/green] in database {}".format(docid, collname, dbname))
        # Update the document with the given id in the given collection in the given database, use mongodb update_one() to update a document
        newDocID = client[dbname][collname].update_one({"_id": docid}, {"$set": jsonobj})
        return newDocID, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())
                      
# Function CheckDomain to check if a domain exists in the provided db, coll and target name, returns docs, a boolean and an error
def CheckDomain(client, dbname, target_name, domain):
    try:
        rprint("[] check if domain [green]{}[/green] exists in collection [green]{}[/green] in database {}".format(domain, target_name, dbname))
        # Query the database for the domain, use QueryDocuments() to query the database
        docs, err = QueryDocuments(client, dbname, target_name, {"domain": domain})
        if err != None:
            return None, None, ierr(err, inspect.currentframe())
        # If no documents are found, return an error
        if docs == "" or docs == None:
            return None, False, None
        # If documents are found, return true
        return docs, True, None
    except Exception as err:
        return None, None, ierr(err, inspect.currentframe())

# function InsertDomain to insert a new document with the provided client, db name, target name, and domain name, returns id of created document and an error
def InsertDomain(client, dbname, collname, domain):
    try:
        # Check if the domain already exists, use CheckDomain() to check if a domain exists
        docs, exists, err = CheckDomain(client, dbname, collname, domain)
        rprint("domain Exists:" + str(exists))
        if err != None:
            return None, ierr(err, inspect.currentframe())
        # If the domain already exists, return an error
        if exists:
            return None, "Domain already exists"
        
        # Insert the domain into the database, use InsertDocuments() to insert documents
        docid, err = InsertDocument(client, dbname, collname, {"domain": domain, "subdomains": []})
        if err != None:
            return None, ierr(err, inspect.currentframe())
        return docid, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

# function CheckSubdomain to check if a subdomain exists in the provided db, coll, target name and domain name, returns the docid if exists, a boolean and an error -> subdomains are found in this format: `{"domain": "domain.com", "subdomains": [{"subdomain": "subdomain.domain.com"},{"subdomain": "subdomain2.domain.com"}]}`
def CheckSubdomain(client, dbname, target_name, domain, subdomain):
    try:
        rprint("[] check if subdomain [green]{}[/green] exists in collection [green]{}[/green] in database {}".format(subdomain, target_name, dbname))
        # first check if the domain exists, use CheckDomain() to check if a domain exists
        docs, exists, err = CheckDomain(client, dbname, target_name, domain)
        if err != None:
            return None, None, ierr(err, inspect.currentframe())
        # If the domain does not exist, return an error
        if not exists:
            return None, False, None
        # If the domain exists, check if the subdomain exists in the subdomains array
        rprint("Found documents:", docs)
        for doc in docs:
            rprint("current doc:", doc)
            # If doc["subdomains"] does not exists or is empty, return false and None
            if "subdomains" not in doc or doc["subdomains"] == None or len(doc["subdomains"]) == 0:
                return doc["_id"], False, None
            # If doc["subdomains"] exists, check if the subdomain exists in the array
            for subdoc in doc["subdomains"]:
                if subdoc["subdomain"] == subdomain:
                    return doc["_id"], True, None
        return None, False, None
    except Exception as err:
        return None, None, ierr(err, inspect.currentframe())

# function AddSubdomain to add a subdomain to the provided client, db name, target name(= collname), domain and subdomain, returns the ID of the updated document and an error
def AddSubdomain(client, dbname, target_name, domain, subdomain):
    try:
        rprint("[] add subdomain [green]{}[/green] to domain [green]{}[/green] in collection [green]{}[/green] in database {}".format(subdomain, domain, target_name, dbname))
        # Check if the subdomain already exists, use CheckSubdomain() to check if a subdomain exists
        docid, exists, err = CheckSubdomain(client, dbname, target_name, domain, subdomain)
        if err != None:
            return None, ierr(err, inspect.currentframe())
        # If the subdomain already exists, return an error
        if exists:
            return None, "Subdomain already exists"
        
        # If the subdomain does not exist, add it to the database, use UpdateOneDocument() to update a document
        if docid == None:
            # If the domain does not exist, create it first, use InsertDomain() to insert a domain
            rprint("Document with domain [green]{}[/green] does not exist, creating it".format(domain))
            docid, err = InsertDomain(client, dbname, target_name, domain)
            if err != None:
                return None, ierr(err, inspect.currentframe())
            # After the domain is created, add the subdomain to the subdomains array
            _, err = UpdateOneDocument(client, dbname, target_name, docid, {"subdomains": [{"subdomain": subdomain}]})
            if err != None:
                return None, ierr(err, inspect.currentframe())
            rprint("Added subdomain: %s" % subdomain)
            return docid, None
        # If the subdomain does exist, add it to the subdomains array
        _, err = UpdateOneDocument(client, dbname, target_name, docid, {"subdomains": [{"subdomain": subdomain}]})
        if err != None:
            return None, ierr(err, inspect.currentframe())
        rprint("Added subdomain: %s" % subdomain)
        return docid, None
    except Exception as err:
        return None, ierr(err, inspect.currentframe())

