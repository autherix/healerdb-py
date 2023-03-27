import inspect
from pymongo import MongoClient
from rich import print
from mod_utils import *
import mod_config
from mongoquery import Query, QueryError

# function CreateClient to create a client on mongodb server using the provided connection string, return client and error
def CreateClient(connstr):
    client = MongoClient(connstr)
    return client, None

# fucntion ExitClient to close the client connection and return the result and error
def ExitClient(client):
    client.close()
    return True, None

# function pingDB to ping the database and return the ping result and error
def pingDB(client):
    pingResult = client.admin.command('ping')
    return pingResult, None

# function conndb to connect to the database and print the result
def conndb(connstr):
    # Connect to the database
    # Create a client and ping the database
    client, err = dbquery.CreateClient(connstr)
    if err != None:
        return None, print(parseError(err))

    pingResult, err = dbquery.pingDB(client)
    if err != None:
        return None, print(parseError(err))
    return f"Ping result: {pingResult}", None
    seperator()

# function FastClient to create a client on mongodb server using the provided connection string, return client and error
def FastClient():
    client = MongoClient(mod_config.GetConnstr()[0])
    return client

# function GetDatabases to get a list of all databases on the server and return the list and error
def GetDatabases(client):
    dblist = client.list_database_names()
    return dblist

# function IsDatabase to check if a database exists on the server and return the result and error
def IsDatabase(client, dbname):
    dblist = client.list_database_names()
    if dbname in dblist:
        return True
    else:
        return False

# function GetCollections to get a list of all collections in a database and return the list and error
def GetCollections(client, db):
    collist = client[db].list_collection_names()
    return collist, None

# function IsCollection to check if a collection exists in a database and return the result and error
def IsCollection(client, db, coll):
    # Check if database exists
    dblist = client.list_database_names()
    if db not in dblist:
        return False, None
    # Check if collection exists
    collist = client[db].list_collection_names()
    if coll in collist:
        return True, None
    else:
        return False, None

# Function PurgeDatabases to delete all databases except admin, config and local and return the list of deleted databases name and error
def PurgeDatabases(client):
    deleted_dbs = []
    dblist = client.list_database_names()
    dblist.remove("admin")
    dblist.remove("config")
    dblist.remove("local")
    for db in dblist:
        client.drop_database(db)
        deleted_dbs.append(db)
    return deleted_dbs

# function CreateDatabase to create a database, create a collection called init
def CreateDatabase(client, dbname):
    db = client[dbname]
    collist = db.list_collection_names()
    if "init" not in collist:
        db.create_collection("init")
    return db, None

# Function CreateCollection to create a collection in a database and return the collection name and error
def CreateCollection(client, dbname, collname):
    db = client[dbname]
    collist = db.list_collection_names()
    if collname not in collist:
        db.create_collection(collname)
    return collname, None

# function DropDatabase to drop a database and return the deleted database name and error 
def DropDatabase(client, dbname):
    client.drop_database(dbname)
    return dbname

# function DropCollection to drop a collection in a database and return the deleted collection's database name and it's own collection name and error
def DropCollection(client, dbname, collname):
    db = client[dbname]
    db.drop_collection(collname)
    return dbname, collname, None

# function PurgeCollections to delete all collections in a database except init and return the list of deleted collections' dbname and deleted collections names (as an array) and error
def PurgeCollections(client, dbname):
    deleted_colls = []
    db = client[dbname]
    collist, err = GetCollections(client, dbname)
    collist.remove("init")
    for coll in collist:
        db.drop_collection(coll)
        deleted_colls.append(coll)
    return dbname, deleted_colls, None

# function AddDocument to add a document to a collection in a database and return the document object's id on success and error
def AddDocument(client, dbname, collname, doc):
    db = client[dbname]
    coll = db[collname]
    doc_id = coll.insert_one(doc).inserted_id
    return doc_id, None

# function RemoveDocument to remove one document from a collection in a database and return the deleted document object's _id and object itself on success and error
def RemoveDocument(client, dbname, collname, doc_id):
    db = client[dbname]
    coll = db[collname]
    doc = coll.find_one_and_delete({"_id": doc_id})
    removed_doc_id = doc["_id"]
    return doc, removed_doc_id, None

# function ListDocuments to list all documents in a collection in a database and return the list of documents id and error
def ListDocuments(client, dbname, collname):
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    docs_ids_list = []
    for doc in docs:
        docs_ids_list.append(doc["_id"])
    return docs_ids_list, None

# function IsDocument to check if a document exists in a collection in a database and return the result and error
def IsDocument(client, dbname, collname, doc_id):
    docs_ids_list = ListDocuments(client, dbname, collname)
    if doc_id in docs_ids_list:
        return True, None
    else:
        return False, None

# function QueryDocuments to query documents in a collection in a database and return the list of documents id and error
def QueryDocuments(client, dbname, collname, query):
    db = client[dbname]
    coll = db[collname]
    docs = coll.find(query)
    docs_ids_list = []
    for doc in docs:
        docs_ids_list.append(doc["_id"])
    return docs_ids_list, None

# function QueryDocumment to query one document in a collection in a database and return the document object and error
def QueryDocument(client, dbname, collname, query):
    db = client[dbname]
    coll = db[collname]
    doc = coll.find_one(query)
    return doc, None

# function UpdateDocument to update one document in a collection in a database and return the updated document object and error
def UpdateDocument(client, dbname, collname, doc_id, new_doc):
    db = client[dbname]
    coll = db[collname]
    doc = coll.find_one_and_update({"_id": doc_id}, {"$set": new_doc})
    # Find the updated document
    doc = coll.find_one({"_id": doc_id})
    return doc, None

# function ListDomains to list all domains in a collection(target) in a database and return the list of domains and error
def ListDomains(client, dbname, collname):
    # Check if collection exists
    collexists, err = IsCollection(client, dbname, collname)
    if err:
        return None, None, err
    if not collexists:
        return None, None, "Collection does not exist"
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    domains_list = []
    for doc in docs:
        if doc["domain"] not in domains_list:
            domains_list.append(doc["domain"])
    return docs, domains_list, None

# function IsDomain to check if a domain exists in a collection(target) in a database and return the result and error
def IsDomain(client, dbname, collname, domain):
    docs, domains_list, err = ListDomains(client, dbname, collname)
    if err:
        return None, None, err
    if domain in domains_list:
        return docs, True, None
    else:
        return docs, False, None

# function AddDomain to add a domain to a collection(target) in a database and return the domain object's id on success and error
def AddDomain(client, dbname, collname, domain):
    # Check if collection exists
    collexists, err = IsCollection(client, dbname, collname)
    if err:
        return None, err
    if not collexists:
        return None, "Collection does not exist"
    # Check if domain exists
    docs, domainexists, err = IsDomain(client, dbname, collname, domain)
    if err:
        return None, err
    if domainexists:
        return None, "Domain already exists"
    # Add domain
    doc = {"domain": domain}
    doc_id, err = AddDocument(client, dbname, collname, doc)
    if err:
        return None, err
    return doc_id, None

# function RemoveDomain to remove one domain from a collection(target) in a database and return the deleted domain object's _id and object itself on success and error
def RemoveDomain(client, dbname, collname, domain):
    # Check if collection exists
    collexists, err = IsCollection(client, dbname, collname)
    if err:
        return None, None, err
    if not collexists:
        return None, None, "Collection does not exist"
    # Check if domain exists
    docs, domainexists, err = IsDomain(client, dbname, collname, domain)
    if err:
        return None, None, err
    if not domainexists:
        return None, None, "Domain does not exist"
    # Remove domain
    doc, doc_id, err = QueryDocument(client, dbname, collname, {"domain": domain})
    if err:
        return None, None, err
    doc, removed_doc_id, err = RemoveDocument(client, dbname, collname, doc_id)
    if err:
        return None, None, err
    return doc, removed_doc_id, None

# function ListSubdomains to list all subdomains in a collection(target) in a database and return the list of subdomains and error
def ListSubdomains(client, dbname, collname, domain):
    # Check if collection exists
    collexists, err = IsCollection(client, dbname, collname)
    if err:
        return None, None, err
    if not collexists:
        return None, None, "Collection does not exist"
    # Check if domain exists
    docs, domainexists, err = IsDomain(client, dbname, collname, domain)
    if err:
        return None, None, err
    if not domainexists:
        return docs, None, "Domain does not exist"

    # Get the list of subdomains (sample doc: `{"domain": "example.com", "subdomains:" [{"subdomain: "sub1.domain.com"}, {"subdomain: "sub2.domain.com"}]}`)
    doc, err = QueryDocument(client, dbname, collname, {"domain": domain})
    if err:
        return None, None, err
    subdomains_list = []
    try:
        doc_subdomains = doc["subdomains"]
    except KeyError:
        return docs, subdomains_list, None
    for subdomain in doc_subdomains:
        subdomains_list.append(subdomain["subdomain"])
    return docs, subdomains_list, None

# function IsSubdomain to check if a subdomain exists in a collection(target) in a database and return the result and error
def IsSubdomain(client, dbname, collname, domain, subdomain):
    docs, subdomains_list, err = ListSubdomains(client, dbname, collname, domain)
    if err:
        return None, None, err
    if subdomain in subdomains_list:
        return docs, True, None
    else:
        return docs, False, None

# function AddSubdomain to add a subdomain to a collection(target) in a database and return the subdomain object's id on success and error
def AddSubdomain(client, dbname, collname, domain, subdomain):
    # Check if subdomain exists
    docs, subdomainexists, err = IsSubdomain(client, dbname, collname, domain, subdomain)
    if err:
        return None, None, err
    if subdomainexists:
        return None, None, "Subdomain already exists"
    # Get the document object
    doc, err = QueryDocument(client, dbname, collname, {"domain": domain})
    if err:
        return None, None, err
    # Add subdomain
    try:
        _ = doc["subdomains"]
    except KeyError:
        doc["subdomains"] = []
    doc["subdomains"].append({"subdomain": subdomain})
    doc, err = UpdateDocument(client, dbname, collname, doc["_id"], doc)
    if err:
        return None, None, err
    return subdomain, doc["_id"], None

# function RemoveSubdomain to remove one subdomain from a collection(target) in a database and return the deleted subdomain object's _id and object itself on success and error
def RemoveSubdomain(client, dbname, collname, domain, subdomain):
    # Check if subdomain exists
    docs, subdomainexists, err = IsSubdomain(client, dbname, collname, domain, subdomain)
    if err:
        return None, None, err
    if not subdomainexists:
        return None, None, "Subdomain does not exist"
    # Get the document object
    doc, err = QueryDocument(client, dbname, collname, {"domain": domain})
    if err:
        return None, None, err
    # Remove subdomain
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            doc["subdomains"].remove(subdomain_obj)
            doc, err = UpdateDocument(client, dbname, collname, doc["_id"], doc)
            if err:
                return None, None, err
            return subdomain_obj, doc["_id"], None
    return None, None, "Subdomain does not exist"

# Function to list all nestedsubdomains in a collection(target) in a database and return the list of nestedsubdomains and error
def ListNestedSubdomains(client, dbname, collname, domain, subdomain):
    # Check if collection exists
    collexists, err = IsCollection(client, dbname, collname)
    if err:
        return None, None, err
    if not collexists:
        return None, None, "Collection does not exist"
    # Check if domain exists
    docs, domainexists, err = IsDomain(client, dbname, collname, domain)
    if err:
        return None, None, err
    if not domainexists:
        return docs, None, "Domain does not exist"
    # Check if subdomain exists
    docs, subdomainexists, err = IsSubdomain(client, dbname, collname, domain, subdomain)
    if err:
        return None, None, err
    if not subdomainexists:
        return docs, None, "Subdomain does not exist"

    # Get the list of nestedsubdomains (sample doc: `{"domain": "example.com", "subdomains:" [{"subdomain: "sub1.domain.com", "subdomains": [{"subdomain": "sub1.sub1.domain.com"}, {"subdomain": "sub2.sub1.domain.com"}]}, {"subdomain: "sub2.domain.com", "subdomains": [{"subdomain": "sub1.sub2.domain.com"}, {"subdomain": "sub2.sub2.domain.com"}]}]}`)
    doc, err = QueryDocument(client, dbname, collname, {"domain": domain})
    if err:
        return None, None, err
    nestedsubdomains_list = []
    try:
        doc_subdomains = doc["subdomains"]
    except KeyError:
        return docs, nestedsubdomains_list, None
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                _ = subdomain_obj["subdomains"]
            except KeyError:
                return docs, nestedsubdomains_list, None
            for nestedsubdomain in subdomain_obj["subdomains"]:
                nestedsubdomains_list.append(nestedsubdomain["subdomain"])
    return docs, nestedsubdomains_list, None

# function IsNestedSubdomain to check if a nestedsubdomain exists in a collection(target) in a database and return the result and error
def IsNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    docs, nestedsubdomains_list, err = ListNestedSubdomains(client, dbname, collname, domain, subdomain)
    if err:
        return None, None, err
    if nestedsubdomain in nestedsubdomains_list:
        return docs, True, None
    else:
        return docs, False, None
    
# function AddNestedSubdomain to add a nestedsubdomain to a collection(target) in a database and return the nestedsubdomain object's id on success and error
def AddNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    # Check if nestedsubdomain exists
    docs, nestedsubdomainexists, err = IsNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain)
    if err:
        return None, None, err
    if nestedsubdomainexists:
        return None, None, "NestedSubdomain already exists"
    # Get the document object
    doc, err = QueryDocument(client, dbname, collname, {"domain": domain})
    if err:
        return None, None, err
    # Add nestedsubdomain
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                _ = subdomain_obj["subdomains"]
            except KeyError:
                subdomain_obj["subdomains"] = []
            subdomain_obj["subdomains"].append({"subdomain": nestedsubdomain})
            doc, err = UpdateDocument(client, dbname, collname, doc["_id"], doc)
            if err:
                return None, None, err
            return nestedsubdomain, doc["_id"], None
    return None, None, "Subdomain does not exist"

# function RemoveNestedSubdomain to remove one nestedsubdomain from a collection(target) in a database and return the deleted nestedsubdomain object's _id and object itself on success and error
def RemoveNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    # Check if nestedsubdomain exists
    docs, nestedsubdomainexists, err = IsNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain)
    if err:
        return None, None, err
    if not nestedsubdomainexists:
        return None, None, "NestedSubdomain does not exist"
    # Get the document object
    doc, err = QueryDocument(client, dbname, collname, {"domain": domain})
    if err:
        return None, None, err
    # Remove nestedsubdomain
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                _ = subdomain_obj["subdomains"]
            except KeyError:
                return None, None, "NestedSubdomain does not exist"
            for nestedsubdomain_obj in subdomain_obj["subdomains"]:
                if nestedsubdomain_obj["subdomain"] == nestedsubdomain:
                    subdomain_obj["subdomains"].remove(nestedsubdomain_obj)
                    doc, err = UpdateDocument(client, dbname, collname, doc["_id"], doc)
                    if err:
                        return None, None, err
                    return nestedsubdomain_obj, doc["_id"], None
    return None, None, "NestedSubdomain does not exist"

# function ListPart, gets client, dbname, collname and parts as *args and returns the members of the parts and error
def ListPart(client, dbname, collname, *args, **kwargs):
    seperator()
    # Check if collection exists
    collexists, err = IsCollection(client, dbname, collname)
    if err:
        return None, err
    if not collexists:
        return None, Exception("Collection does not exist")
    
    # if len of kwargs is 0, then return all the documents in the collection
    print("kwargs: ", kwargs)
    if len(kwargs) == 0:
        docs_ids, err = ListDocuments(client, dbname, collname)
        if err:
            return None, err
        print("no kwargs found, returning all docs inside collection...")
        return docs_ids, None

    # print the first pair in kwargs, use NthKey function
    print("NthKey(kwargs, 0): ", NthKey(kwargs, 0))

    doc, err = QueryDocument(client, dbname, collname, NthKey(kwargs, 0))
    if err:
        return None, err
    print("data after filter with kwargs[0]: ", doc)
    # if doc is empty then return None
    if not doc:
        return None, Exception("No document found")
    doc_id = doc["_id"]
    # shift kwargs 1 to the left
    kwargs = ShiftLeft(kwargs, 1)
    print("kwargs after shift: ", kwargs)

    # if len of args is 0, then return the document
    if len(args) == 0:
        return doc, None
    
    # iterate over the args and get the members of the parts in both args and kwargs
    for i, arg in enumerate(args):
        try:
            print("selecting part: ", arg, " from the document:", doc)
            doc = doc[arg]
            print("current doc after selection: ", doc)
        except KeyError as err:
            return None, Exception("Cannot find the part {} in the document".format(arg))
        except TypeError as err:
            return None, Exception("Cannot find the part {} in the document".format(arg))
        # if len of kwargs is 0, then return the doc
        print("kwargs: ", kwargs)
        if len(kwargs) == 0:
            print("kwargs is empty, returning doc: ", doc)
            return doc, None
        # if len of kwargs is not 0, then use kwargs[0] as query to find the document(e.g. {"subdomain": "sub1"})
        queryjson = Query(NthKey(kwargs, 0))
        try:
            doc = list(filter(Query(NthKey(kwargs, 0)).match, doc))[0]
        except IndexError as err:
            return {}, None
        print("data after filter with {} : {}".format(NthKey(kwargs, 0), doc))
        # doc, err = QueryDocument(client, dbname, collname, NthKey(kwargs, 0))
        if err:
            return None, err
        # if doc is empty then return None
        if not doc:
            return None, Exception("No document found")
        # shift kwargs 1 to the left
        kwargs = ShiftLeft(kwargs, 1)
        print("kwargs after shift: ", kwargs)
    # return the doc
    return doc, None

# function GetInfo, gets client, dbname, collname, a json filter (as string, e.g. `{"domain": "domain1.com"}`) and parts as *args (all members of args are strings) and returns the members of the parts and error
def GetInfo(client, dbname, collname, filterjson=None, *args):
    # Check if collection exists
    collexists, err = IsCollection(client, dbname, collname)
    if err:
        return None, err
    if not collexists:
        return None, Exception("Collection does not exist")

    # If filterjson is empty, then return all the documents ids in the collection
    if not filterjson:
        docs_ids, err = ListDocuments(client, dbname, collname)
        if err:
            return None, err
        return docs_ids, None

    # Convert filterjson to json
    filterjson = json.loads(filterjson)
    # Get the document object
    doc, err = QueryDocument(client, dbname, collname, filterjson)
    if err:
        return None, err
    # if doc is empty then return None
    if not doc:
        return None, Exception("No document found")
    
    # if len of args is 0, then return the document
    if len(args) == 0:
        return doc, None
    
    # From now on, we have a document and we need to get the members of the parts in args, so we use GetFromJson function to get the members of the parts in args
    doc, err = GetFromJson(doc, *args)
    if err:
        return None, err
    return doc, None

