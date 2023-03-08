import inspect
from pymongo import MongoClient
from rich import print
from mod_utils import *

# function CreateClient to create a client on mongodb server using the provided connection string, return client and error
def CreateClient(connstr):
    try:
        client = MongoClient(connstr)
        return client, None
    except Exception as err:
        return None, err

# fucntion ExitClient to close the client connection and return the result and error
def ExitClient(client):
    try:
        client.close()
        return True, None
    except Exception as err:
        return None, err

# function pingDB to ping the database and return the ping result and error
def pingDB(client):
    try:
        pingResult = client.admin.command('ping')
        return pingResult, None
    except Exception as err:
        return None, err

# function GetDatabases to get a list of all databases on the server and return the list and error
def GetDatabases(client):
    try:
        dblist = client.list_database_names()
        return dblist, None
    except Exception as err:
        return None, err

# function IsDatabase to check if a database exists on the server and return the result and error
def IsDatabase(client, dbname):
    try:
        dblist = client.list_database_names()
        if dbname in dblist:
            return True, None
        else:
            return False, None
    except Exception as err:
        return None, err

# function GetCollections to get a list of all collections in a database and return the list and error
def GetCollections(client, db):
    try:
        collist = client[db].list_collection_names()
        return collist, None
    except Exception as err:
        return None, err

# function IsCollection to check if a collection exists in a database and return the result and error
def IsCollection(client, db, coll):
    try:
        collist = client[db].list_collection_names()
        if coll in collist:
            return True, None
        else:
            return False, None
    except Exception as err:
        return None, err

# Function PurgeDatabases to delete all databases except admin, config and local and return the list of deleted databases name and error
def PurgeDatabases(client):
    try:
        deleted_dbs = []
        dblist = client.list_database_names()
        dblist.remove("admin")
        dblist.remove("config")
        dblist.remove("local")
        for db in dblist:
            client.drop_database(db)
            deleted_dbs.append(db)
        return deleted_dbs, None
    except Exception as err:
        return deleted_dbs, err

# function CreateDatabase to create a database, create a collection called init
def CreateDatabase(client, dbname):
    try:
        db = client[dbname]
        collist = db.list_collection_names()
        if "init" not in collist:
            db.create_collection("init")
        return db, None
    except Exception as err:
        return None, err

# Function CreateCollection to create a collection in a database and return the collection name and error
def CreateCollection(client, dbname, collname):
    try:
        db = client[dbname]
        collist = db.list_collection_names()
        if collname not in collist:
            db.create_collection(collname)
        return collname, None
    except Exception as err:
        return None, err

# function DropDatabase to drop a database and return the deleted database name and error 
def DropDatabase(client, dbname):
    try:
        client.drop_database(dbname)
        return dbname, None
    except Exception as err:
        return None, err

# function DropCollection to drop a collection in a database and return the deleted collection's database name and it's own collection name and error
def DropCollection(client, dbname, collname):
    try:
        db = client[dbname]
        db.drop_collection(collname)
        return dbname, collname, None
    except Exception as err:
        return None, None, err

# function PurgeCollections to delete all collections in a database except init and return the list of deleted collections' dbname and deleted collections names (as an array) and error
def PurgeCollections(client, dbname):
    try:
        deleted_colls = []
        db = client[dbname]
        collist, err = GetCollections(client, dbname)
        collist.remove("init")
        for coll in collist:
            db.drop_collection(coll)
            deleted_colls.append(coll)
        return dbname, deleted_colls, None
    except Exception as err:
        return dbname, deleted_colls, err

# function AddDocument to add a document to a collection in a database and return the document object's id on success and error
def AddDocument(client, dbname, collname, doc):
    try:
        db = client[dbname]
        coll = db[collname]
        doc_id = coll.insert_one(doc).inserted_id
        return doc_id, None
    except Exception as err:
        return None, err

# function RemoveDocument to remove one document from a collection in a database and return the deleted document object's _id and object itself on success and error
def RemoveDocument(client, dbname, collname, doc_id):
    try:
        db = client[dbname]
        coll = db[collname]
        doc = coll.find_one_and_delete({"_id": doc_id})
        removed_doc_id = doc["_id"]
        return doc, removed_doc_id, None
    except Exception as err:
        return None, None, err

# function ListDocuments to list all documents in a collection in a database and return the list of documents id and error
def ListDocuments(client, dbname, collname):
    try:
        db = client[dbname]
        coll = db[collname]
        docs = coll.find()
        docs_ids_list = []
        for doc in docs:
            docs_ids_list.append(doc["_id"])
        return docs_ids_list, None
    except Exception as err:
        return None, err

# function IsDocument to check if a document exists in a collection in a database and return the result and error
def IsDocument(client, dbname, collname, doc_id):
    try:
        docs_ids_list = ListDocuments(client, dbname, collname)
        if doc_id in docs_ids_list:
            return True, None
        else:
            return False, None
    except Exception as err:
        return None, err

# function QueryDocuments to query documents in a collection in a database and return the list of documents id and error
def QueryDocuments(client, dbname, collname, query):
    try:
        db = client[dbname]
        coll = db[collname]
        docs = coll.find(query)
        docs_ids_list = []
        for doc in docs:
            docs_ids_list.append(doc["_id"])
        return docs_ids_list, None
    except Exception as err:
        return None, err

# function QueryDocumment to query one document in a collection in a database and return the document object and error
def QueryDocument(client, dbname, collname, query):
    try:
        db = client[dbname]
        coll = db[collname]
        doc = coll.find_one(query)
        return doc, None
    except Exception as err:
        return None, err

# function UpdateDocument to update one document in a collection in a database and return the updated document object and error
def UpdateDocument(client, dbname, collname, doc_id, new_doc):
    try:
        db = client[dbname]
        coll = db[collname]
        doc = coll.find_one_and_update({"_id": doc_id}, {"$set": new_doc})
        return doc, None
    except Exception as err:
        return None, err
