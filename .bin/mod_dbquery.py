from pymongo import MongoClient
from rich import print

# function CreateClient to create a client on mongodb server using the provided connection string, return client and error if any
def CreateClient(connstr):
    try:
        client = MongoClient(connstr)
        return client, None
    except Exception as err:
        return None, err

# function DisconnectClient to disconnect the client from mongodb server
def DisconnectClient(client):
    client.close()

# function PingClient to ping the client to the mongodb server, returns a boolean and an error
def PingClient(client):
    try:
        return client.admin.command('ping'), None
    except Exception as err:
        return None, err

# function GetDatabases to get client and return list of databases names and error if any
def GetDatabases(client):
    try:
        return client.list_database_names(), None
    except Exception as err:
        return None, err

# function CheckDatabase to check if a database with the given name exists, returns a boolean and an error
def CheckDatabase(client, dbname):
    try:
        return dbname in client.list_database_names(), None
    except Exception as err:
        return None, err

# function PurgeDatabases to delete all the databases in the database except the admin and config databases, returns an error
def PurgeDatabases(client):
    try:
        for db in client.list_database_names():
            if db not in ["admin", "config", "local"]:
                client.drop_database(db)
        return None
    except Exception as err:
        return err

# function CheckCollection to check if a collection with the given name exists in the given database, returns a boolean and an error
def CheckCollection(client, dbname, collname):
    try:
        return collname in client[dbname].list_collection_names(), None
    except Exception as err:
        return None, err

# function CheckDocument to check if a document with the given id exists in the given collection in the given database, returns a boolean and an error
def CheckDocument(client, dbname, collname, docid):
    try:
        return client[dbname][collname].find_one({"_id": docid}) != None, None
    except Exception as err:
        return None, err

# function CreateDocument to create a document in the given collection in the given database, with the provided json string of the document, returns the _id of the created document and an error
def CreateDocument(client, dbname, collname, doc):
    try:
        return client[dbname][collname].insert_one(doc).inserted_id, None
    except Exception as err:
        return None, err

# function CreateCollection to create a collection, with the provided name, in the given database, returns collection name and error 
def CreateCollection(client, dbname, collname):
    try:
        return client[dbname].create_collection(collname).name, None
    except Exception as err:
        return None, err

# function CreateDatabase to create a database, with the provided name, returns an error -> for creating a database, it just creates a collection in the database with the name 'exists' and the content as 'exists': true
def CreateDatabase(client, dbname):
    try:
        return CreateCollection(client, dbname, "exists")
    except Exception as err:
        return None, err

# function DropCollection to drop a collection, with the provided name(removes if exists), in the given database, returns an error
def DropCollection(client, dbname, collname):
    try:
        client[dbname].drop_collection(collname)
        return None
    except Exception as err:
        return err

# function DropDatabase to drop a database, with the provided database name(removes database if exists), returns an error
def DropDatabase(client, dbname):
    try:
        client.drop_database(dbname)
        return None
    except Exception as err:
        return err

# function GetCollections to get the the client to the database, a database name, fetches all collection names in the given database and returns an array containing the names of the collections and an error
def GetCollections(client, dbname):
    try:
        return client[dbname].list_collection_names(), None
    except Exception as err:
        return None, err

# function GetDocuments to get the the client to the database, a database name and a collection name, fetches all documents in the given collection, converts each document to a string of json object and returns an array containing the json objects and an error
def GetDocuments(client, dbname, collname):
    try:
        docs = []
        for doc in client[dbname][collname].find():
            docs.append(doc)
        return docs, None
    except Exception as err:
        return None, err

# function GetDocument to get client to database, database name, collection name and document id, fetches the document with the given id from the given collection in the given database, converts the document to a string of json object and returns the json object and an error
def GetDocument(client, dbname, collname, docid):
    try:
        return client[dbname][collname].find_one({"_id": docid}), None
    except Exception as err:
        return None, err

# function CountDocuments to get 

# function DeleteDocument to get client to database, database name, collection name and document id, deletes the document with the given id from the given collection in the given database, returns an error
def DeleteDocument(client, dbname, collname, docid):
    try:
        client[dbname][collname].delete_one({"_id": docid})
        return None
    except Exception as err:
        return err

# function InsertDocument to get client, db, coll, and json document, inserts the document into the collection, returns an error
def InsertDocument(client, dbname, collname, doc):
    try:
        client[dbname][collname].insert_one(doc)
        return None
    except Exception as err:
        return err  

# function InsertDocuments to get client, db, coll, document id and document string, inserts the documents into the collection in the database, returns an array containing the _id of the added documents and an error
def InsertDocuments(client, dbname, collname, docs):
    try:
        return client[dbname][collname].insert_many(docs).inserted_ids, None
    except Exception as err:
        return None, err

# function AddUniqueIndex to add unique index to a collection in a database, returns an error
def AddUniqueIndex(client, dbname, collname, index):
    try:
        client[dbname][collname].create_index(index, unique=True)
        return None
    except Exception as err:
        return err

# function CheckTarget to check if a collection exists in the database, returns a boolean and an error
def CheckTarget(client, dbname, target):
    try: 
        # Query the database for the collection, use CheckCollection() to check if a collection exists
        return CheckCollection(client, dbname, target)
    except Exception as err:
        return None, err

# function AddTarget to add a collection to the database, returns an error
def AddTarget(client, dbname, target):
    try:
        # Check if the target already exists
        exists, err = CheckTarget(client, dbname, target)
        if err != None:
            return err
        # If the target already exists, return an error 
        if exists:
            return "Target already exists"
        
        # Add a collection with target name to the database, use CreateCollection() to create a collection
        _, err = CreateCollection(client, dbname, target)
        if err != None:
            return "Error adding target: %s" % err
        print("Added target: %s" % target)
        return None
    except Exception as err:
        return err

# function QueryDocuments to query the database, parameters are database name, collection name, query object, returns a json objects and an error
def QueryDocuments(client, dbname, collname, query):
    try:
        # Query the database for the documents, use GetDocuments() to get all documents in a collection
        docs, err = GetDocuments(client, dbname, collname)
        if err != None:
            return None, err
        # If no documents are found, return an error
        if len(docs) == 0:
            return None, "No documents found"
        
        # Query the documents for the given query object
        results = []
        for doc in docs:
            if all(item in doc.items() for item in query.items()):
                results.append(doc)
        return results, None
    except Exception as err:
        return None, err

# function UpdateOneDocument  to update a document in the database, returns ID of successfully updated document and an error -> get client, db, collection name, document id, object(as json) in parameters
def UpdateOneDocument(client, dbname, collname, docid, obj):
    try:
        newDocID = client[dbname][collname].update_one({"_id": docid}, {"$set": obj})
        return newDocID, None
    except Exception as err:
        return None, err
