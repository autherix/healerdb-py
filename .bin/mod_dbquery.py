import inspect, re
from pymongo import MongoClient
# from rich import print
from mod_utils import *
import mod_config
from mongoquery import Query, QueryError
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

# function CreateClient to create a client on mongodb server using the provided connection string, return client
def CreateClient(connstr):
    client = MongoClient(connstr)
    return client, None

# fucntion ExitClient to close the client connection and return the result
def ExitClient(client):
    client.close()
    return True, None

# function pingDB to ping the database and return the ping result
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

# function FastClient to create a client on mongodb server using the provided connection string, return client
def FastClient():
    client = MongoClient(mod_config.GetConnstr()[0])
    return client

# function GetDatabases to get a list of all databases on the server and return the list
def GetDatabases(client):
    dblist = client.list_database_names()
    return dblist

# function IsDatabase to check if a database exists on the server and return the result
def IsDatabase(client, dbname):
    dblist = client.list_database_names()
    if dbname in dblist:
        return True
    else:
        return False

# function GetCollections to get a list of all collections in a database and return the list
def GetCollections(client, db):
    collist = client[db].list_collection_names()
    return collist

# function IsCollection to check if a collection exists in a database and return the result
def IsCollection(client, db, coll):
    # Check if database exists
    dblist = client.list_database_names()
    if db not in dblist:
        return False
    # Check if collection exists
    collist = client[db].list_collection_names()
    if coll in collist:
        return True
    else:
        return False

# Function PurgeDatabases to delete all databases except admin, config and local and return the list of deleted databases name
def PurgeDatabases(client):
    deleted_dbs = []
    dblist = client.list_database_names()
    dblist.remove("admin")
    dblist.remove("config")
    dblist.remove("local")
    dblist.remove("bbplats")
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
    return db.name

# Function CreateCollection to create a collection in a database and return the collection name
def CreateCollection(client, dbname, collname):
    db = client[dbname]
    collist = db.list_collection_names()
    if collname not in collist:
        db.create_collection(collname)
    return collname

# function DropDatabase to drop a database and return the deleted database name 
def DropDatabase(client, dbname):
    client.drop_database(dbname)
    return dbname

# function DropCollection to drop a collection in a database and return the deleted collection's database name and it's own collection name
def DropCollection(client, dbname, collname):
    db = client[dbname]
    db.drop_collection(collname)
    return dbname, collname

# function PurgeCollections to delete all collections in a database except init and return the list of deleted collections' dbname and deleted collections names (as an array)
def PurgeCollections(client, dbname):
    deleted_colls = []
    db = client[dbname]
    collist = GetCollections(client, dbname)
    collist.remove("init")
    for coll in collist:
        db.drop_collection(coll)
        deleted_colls.append(coll)
    return deleted_colls

# function AddDocument to add a document to a collection in a database and return the document object's id on success
def AddDocument(client, dbname, collname, doc):
    db = client[dbname]
    coll = db[collname]
    # If doc is string, convert it to json
    if isinstance(doc, str):
        try:
            doc = json.loads(doc)
        except:
            raise Exception("Invalid JSON")
    doc_id = coll.insert_one(doc).inserted_id
    return doc_id

# function RemoveDocument to remove one document from a collection in a database and return the deleted document object's _id and object itself on success
def RemoveDocument(client, dbname, collname, doc_id):
    db = client[dbname]
    coll = db[collname]
    doc = coll.find_one_and_delete({"_id": ObjectId(doc_id)})
    if doc is None:
        return []
    removed_doc_id = doc["_id"]
    return doc

# function ListDocuments to list all documents in a collection in a database and return the list of documents id
def ListDocuments(client, dbname, collname):
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    docs_ids_list = []
    for doc in docs:
        docs_ids_list.append(doc["_id"])
    return docs_ids_list

# function IsDocument to check if a document exists in a collection in a database and return the result
def IsDocument(client, dbname, collname, doc_id):
    docs_ids_list = ListDocuments(client, dbname, collname)
    for doc in docs_ids_list:
        if str(doc) == str(doc_id):
            return True
    return False

# function QueryDocuments to query documents in a collection in a database and return the list of documents id
def QueryDocuments(client, dbname, collname, query):
    db = client[dbname]
    coll = db[collname]
    # If query is string, convert it to json
    if isinstance(query, str):
        try:
            query = json.loads(query)
        except:
            raise Exception("Invalid query - Cannot convert to JSON")
    docs = coll.find(query)
    docs_ids_list = []
    for doc in docs:
        docs_ids_list.append(doc["_id"])
    return docs_ids_list

# function QueryDocumment to query one document in a collection in a database and return the document object
def QueryDocument(client, dbname, collname, query):
    db = client[dbname]
    coll = db[collname]
    # If query is string, convert it to json
    if isinstance(query, str):
        try:
            query = json.loads(query)
        except:
            raise Exception("Invalid query - Cannot convert to JSON")
    doc = coll.find_one(query)
    return doc

# function UpdateDocument to update one document in a collection in a database and return the updated document object
def UpdateDocumentWithQuery(client, dbname, collname, query, new_doc):
    db = client[dbname]
    coll = db[collname]
    # If query is string, convert it to json
    if isinstance(query, str):
        try:
            query = json.loads(query)
        except:
            raise Exception("Invalid query - Cannot convert to JSON")
    # If new_doc is string, convert it to json
    if isinstance(new_doc, str):
        try:
            new_doc = json.loads(new_doc)
        except:
            raise Exception("Invalid new_doc - Cannot convert to JSON")
    doc = coll.find_one_and_update(query, {"$set": new_doc}, return_document=ReturnDocument.AFTER)
    return doc

# function UpdateDocument to update one document in a collection in a database and return the updated document object
def UpdateDocumentByID(client, dbname, collname, doc_id, new_doc):
    # Use UpdateDocumentWithQuery to update the document
    query = {"_id": ObjectId(doc_id)}
    doc = UpdateDocumentWithQuery(client, dbname, collname, query, new_doc)
    return doc

# function UpdateDocumentsWithQuery to update documents in a collection in a database and return the updated documents objects
def UpdateDocumentsWithQuery(client, dbname, collname, query, new_doc):
    db = client[dbname]
    coll = db[collname]
    # If query is string, convert it to json
    if isinstance(query, str):
        try:
            query = json.loads(query)
        except:
            raise Exception("Invalid query - Cannot convert to JSON")
    # If new_doc is string, convert it to json
    if isinstance(new_doc, str):
        try:
            new_doc = json.loads(new_doc)
        except:
            raise Exception("Invalid new_doc - Cannot convert to JSON")
    docs = coll.find(query)
    updated_docs = []
    for doc in docs:
        updated_doc = coll.find_one_and_update({"_id": doc["_id"]}, {"$set": new_doc}, return_document=ReturnDocument.AFTER)
        updated_docs.append(updated_doc)
    return updated_docs

# function PurgeDocuments to remove all documents in a collection in a database and return the list of deleted documents IDs
def PurgeDocuments(client, dbname, collname):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    deleted_docs = []
    for doc in docs:
        deleted_doc = RemoveDocument(client, dbname, collname, doc["_id"])
        deleted_docs.append(deleted_doc["_id"])
    return deleted_docs

# function ListDomains to list all domains in a collection(target) in a database and return the list of domains
def ListDomains(client, dbname, collname):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    domains_list = []
    for doc in docs:
        if doc["domain"] not in domains_list:
            domains_list.append(doc["domain"])
    return docs, domains_list

# function IsDomain to check if a domain exists in a collection(target) in a database and return the result
def IsDomain(client, dbname, collname, domain):
    docs, domains_list = ListDomains(client, dbname, collname)
    if domain in domains_list:
        return docs, True
    else:
        return docs, False

# function AddDomain to add a domain to a collection(target) in a database and return the domain object's id on success
def AddDomain(client, dbname, collname, domain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create db and collection
        CreateCollection(client, dbname, collname)
        
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if domainexists:
        return ""
    # Add domain
    doc = {"domain": domain}
    doc_id = AddDocument(client, dbname, collname, doc)
    return doc_id

# function GetDomain to get one domain from a collection(target) in a database and return the domain object, Use QueryDocument to get the domain object
def GetDomain(client, dbname, collname, domain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return ""
    # Get domain
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    return doc

# function RemoveDomain to remove one domain from a collection(target) in a database and return the deleted domain object's _id and object itself on success
def RemoveDomain(client, dbname, collname, domain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return ""
    # Remove domain
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    doc_id = doc["_id"]
    doc = RemoveDocument(client, dbname, collname, doc_id)
    return doc, doc["_id"]

# function InitDomain creates a domain if not exists, if exists, removes all sub-parts in it and returns the document object
def InitDomain(client, dbname, collname, domain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
        
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if domainexists:
        # Remove domain Using RemoveDomain
        deleted_doc, doc_id = RemoveDomain(client, dbname, collname, domain)
        # Add domain
        doc = {'_id': ObjectId(doc_id), 'domain': domain, 'subdomains': []}
        # Add domain
        doc_id = AddDomain(client, dbname, collname, domain)
    else:
        # Add domain
        doc = {"domain": domain, "subdomains": []}
        doc_id = AddDomain(client, dbname, collname, domain)
        doc = GetDomain(client, dbname, collname, domain)
    return doc, doc_id

# function PurgeDomains to remove all domains in a collection(target) in a database and return the list of deleted domains ['domain']
def PurgeDomains(client, dbname, collname):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    deleted_docs = []
    for doc in docs:
        deleted_doc, deletd_doc_id = RemoveDomain(client, dbname, collname, doc["domain"])
        deleted_docs.append(deleted_doc["domain"])
    return deleted_docs

# function ListSubdomains to list all subdomains in a collection(target) in a database and return the list of subdomains
def ListSubdomains(client, dbname, collname, domain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    doc, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return "", []

    # Get the list of subdomains (sample doc: `{"domain": "example.com", "subdomains:" [{"subdomain: "sub1.domain.com"}, {"subdomain: "sub2.domain.com"}]}`)
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    subdomains_list = []
    try:
        doc_subdomains = doc["subdomains"]
    except KeyError:
        return doc, subdomains_list
    for subdomain in doc_subdomains:
        subdomains_list.append(subdomain["subdomain"])
    return doc, subdomains_list

# function IsSubdomain to check if a subdomain exists in a collection(target) in a database and return the result
def IsSubdomain(client, dbname, collname, domain, subdomain):
    doc, subdomains_list = ListSubdomains(client, dbname, collname, domain)
    if subdomain in subdomains_list:
        return doc, True
    else:
        return doc, False

# function AddSubdomain to add a subdomain to a collection(target) in a database and return the subdomain object's id on success
def AddSubdomain(client: MongoClient, dbname: str, collname: str, domain: str, subdomain: str, live: bool = False):
    # Check if subdomain exists
    doc, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    # Verified -> this doc is a real whole documnet
    if subdomainexists:
        return subdomain
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        # Add domain
        doc_id = AddDomain(client, dbname, collname, domain)
        doc = GetDomain(client, dbname, collname, domain)
    # Add subdomain
    try:
        doc_subdomains = doc["subdomains"]
    except KeyError:
        doc["subdomains"] = []
    doc["subdomains"].append({"subdomain": subdomain})
    # doc["subdomains"].append({"subdomain": subdomain, "live": live})
    doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
    return subdomain

# function AddSubdomains to add a list of subdomains to a collection(target) in a database and return the list of subdomain objects' id on success
def AddSubdomains(client: MongoClient, dbname: str, collname: str, domain: str, subdomains: str):
    # if subdomains starts with "/tmp/", read the file and get the content and store each line's content as an item in subdomains list
    if subdomains.startswith("/tmp/"):
        # Read the file
        with open(subdomains, "r") as f:
            subdomains = f.read()
    # Make all of them seperated by space 
    subdomains = subdomains.replace("\n", " ")

    # Split subdomains string into a list of subdomains, use space as delimiter(ant space character, one space, two spaces, tab, etc.)
    subdomains = re.split(r'\s+', subdomains)
    # Create an empty list to store added subdomains
    
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        # Add domain
        doc_id = AddDomain(client, dbname, collname, domain)
        doc = GetDomain(client, dbname, collname, domain)

    added_subdomains = []
    # Add subdomains
    for subdomain in subdomains:
        # Check if subdomain exists
        doc, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
        # Verified -> this doc is a real whole documnet
        if subdomainexists:
            updated_doc = None
        else:
            # Add subdomain
            try:
                doc_subdomains = doc["subdomains"]
            except KeyError:
                doc["subdomains"] = []
            doc["subdomains"].append({"subdomain": subdomain})
            # doc["subdomains"].append({"subdomain": subdomain, "live": live})
            updated_doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
            # If doc is not empty, add it to the list
            added_subdomains.append(subdomain)
    return added_subdomains

# function RemoveSubdomain to remove one subdomain from a collection(target) in a database and return the deleted subdomain object's _id and object itself on success
def RemoveSubdomain(client: MongoClient, dbname: str, collname: str, domain: str, subdomain: str):
    # Check if subdomain exists
    docs, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        return "", ""
    # Get the document object
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    # Remove subdomain
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            doc["subdomains"].remove(subdomain_obj)
            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
            return subdomain_obj, doc["_id"]
    return "", ""

# Function to list all nestedsubdomains in a collection(target) in a database and return the list of nestedsubdomains
def ListNestedSubdomains(client, dbname, collname, domain, subdomain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        raise Exception("Domain does not exist")
    # Check if subdomain exists
    docs, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        raise Exception("Subdomain does not exist")

    # Get the list of nestedsubdomains (sample doc: `{"domain": "example.com", "subdomains:" [{"subdomain: "sub1.domain.com", "subdomains": [{"subdomain": "sub1.sub1.domain.com"}, {"subdomain": "sub2.sub1.domain.com"}]}, {"subdomain: "sub2.domain.com", "subdomains": [{"subdomain": "sub1.sub2.domain.com"}, {"subdomain": "sub2.sub2.domain.com"}]}]}`)
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    nestedsubdomains_list = []
    try:
        doc_subdomains = doc["subdomains"]
    except KeyError:
        return docs, nestedsubdomains_list
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                _ = subdomain_obj["subdomains"]
            except KeyError:
                return docs, nestedsubdomains_list
            for nestedsubdomain in subdomain_obj["subdomains"]:
                nestedsubdomains_list.append(nestedsubdomain["subdomain"])
    return docs, nestedsubdomains_list

# function IsNestedSubdomain to check if a nestedsubdomain exists in a collection(target) in a database and return the result
def IsNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    docs, nestedsubdomains_list = ListNestedSubdomains(client, dbname, collname, domain, subdomain)
    if nestedsubdomain in nestedsubdomains_list:
        return docs, True
    else:
        return docs, False
    
# function AddNestedSubdomain to add a nestedsubdomain to a collection(target) in a database and return the nestedsubdomain object's id on success
def AddNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    # type: (CosmosClient, str, str, str, str, str) -> Tuple[str, str]
    # Check if nestedsubdomain exists
    docs, nestedsubdomainexists = IsNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain)
    if nestedsubdomainexists:
        raise Exception("Nestedsubdomain already exists")
    # Get the document object
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    # Add nestedsubdomain
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                _ = subdomain_obj["subdomains"]
            except KeyError:
                subdomain_obj["subdomains"] = []
            subdomain_obj["subdomains"].append({"subdomain": nestedsubdomain})
            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
            return nestedsubdomain, doc["_id"]
    raise Exception("Subdomain does not exist")

# function RemoveNestedSubdomain to remove one nestedsubdomain from a collection(target) in a database and return the deleted nestedsubdomain object's _id and object itself on success
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

# function ListUrls to list all urls in a domain in a collection(target) in a database and return the list of urls
def ListUrls(client, dbname, collname, domain, subdomain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return "", []
    # Check if subdomain exists
    docs, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        return "", []

    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    urls_list = []
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                doc_urls = subdomain_obj["urls"]
            except KeyError:
                return docs, urls_list
            for url_obj in subdomain_obj["urls"]:
                urls_list.append(url_obj["url"])
    return docs, urls_list

# function IsUrl to check if a url exists in a collection(target) in a database and return the result
def IsUrl(client, dbname, collname, domain, subdomain, url):
    docs, urls_list = ListUrls(client, dbname, collname, domain, subdomain)
    if url in urls_list:
        return docs, True
    else:
        return docs, False

# function AddUrl to add a url to a collection(target) in a database and return the url object's id on success
def AddUrls(client, dbname, collname, domain, subdomain, urls):
    # Split urls by " "
    urls_list = re.split(r"\s+", urls)

    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        # Add domain
        doc_id = AddDomain(client, dbname, collname, domain)
        doc = GetDomain(client, dbname, collname, domain)
    # Check if subdomain exists
    docs, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        # Add subdomain
        doc_id = AddSubdomain(client, dbname, collname, domain, subdomain)
        doc = GetDomain(client, dbname, collname, domain)

    # set the doc using GetDomain
    doc = GetDomain(client, dbname, collname, domain)

    added_urls = []
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                doc_urls = subdomain_obj["urls"]
            except KeyError:
                subdomain_obj["urls"] = []
            for url in urls_list:
                if not IsUrl(client, dbname, collname, domain, subdomain, url)[1]:
                    subdomain_obj["urls"].append({"url": url})
                    added_urls.append(url)
            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
    return added_urls

# function RemoveUrl to remove a url from a collection(target) in a database and return the deleted url object's _id and object itself on success
def RemoveUrl(client, dbname, collname, domain, subdomain, url):
    # Check if url exists
    docs, urlexists = IsUrl(client, dbname, collname, domain, subdomain, url)
    if not urlexists:
        return "", ""
    # Get the document object
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    # Remove url
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            for url_obj in subdomain_obj["urls"]:
                if url_obj["url"] == url:
                    subdomain_obj["urls"].remove(url_obj)
                    doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
                    return url_obj, doc["_id"]

# function ListUrlParameters to list all url parameters in a domain in a collection(target) in a database and return the list of url parameters
def ListUrlParameters(client, dbname, collname, domain, subdomain, url):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    _, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return "", []
    # Check if subdomain exists
    _, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        return "", []
    # Check if url exists
    _, urlexists = IsUrl(client, dbname, collname, domain, subdomain, url)
    if not urlexists:
        return "", []

    # Get the list of urls - sample doc:
    # {
    #     "domain": "example.com",
    #     "subdomains": [
    #         {
    #             "subdomain": "www",
    #             "urls": [
    #                 {
    #                     "url": "https://example.com/about",
    #                     "parameters": [
    #                         {
    #                             "parameter": "id"
    #                         },
    #                         {
    #                             "parameter": "name"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    parameters_list = []
    try:
        subdomains = doc["subdomains"]
    except KeyError:
        return "", []
    for subdomain_obj in subdomains:
        if subdomain_obj["subdomain"] == subdomain:
            try: 
                urls = subdomain_obj["urls"]
            except KeyError:
                return "", []
            for url_obj in urls:
                if url_obj["url"] == url:
                    try:
                        parameters = url_obj["parameters"]
                    except KeyError:
                        return "", []
                    for parameter_obj in parameters:
                        if parameter_obj["parameter"] not in parameters_list:
                            parameters_list.append(parameter_obj["parameter"])
    return doc, parameters_list

# function IsUrlParameter to check if a url parameter exists in a collection(target) in a database and return the result
def IsUrlParameter(client, dbname, collname, domain, subdomain, url, parameter):
    docs, parameters_list = ListUrlParameters(client, dbname, collname, domain, subdomain, url)
    if parameter in parameters_list:
        return docs, True
    else:
        return docs, False

# function AddUrlParameters to add a list of url parameters to a collection(target) in a database and return the list of url parameter objects' id on success
def AddUrlParameters(client, dbname, collname, domain, subdomain, url, parameters):
    # Split parameters by " "
    parameters_list = re.split(r"\s+", parameters)

    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        # Add domain
        doc_id = AddDomain(client, dbname, collname, domain)
        doc = GetDomain(client, dbname, collname, domain)
    # Check if subdomain exists
    docs, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        # Add subdomain
        doc_id = AddSubdomain(client, dbname, collname, domain, subdomain)
        doc = GetDomain(client, dbname, collname, domain)
    # Check if url exists
    docs, urlexists = IsUrl(client, dbname, collname, domain, subdomain, url)
    if not urlexists:
        # Add url
        doc_id = AddUrl(client, dbname, collname, domain, subdomain, url)
        doc = GetDomain(client, dbname, collname, domain)

    # set the doc using GetDomain
    doc = GetDomain(client, dbname, collname, domain)
    added_parameters = []

    # Urls should be added inside a subdomain + handle duplicates + handle KeyErrors when subdomain["urls"] doesn't exist
    subdomains = doc["subdomains"]
    for subdomain_obj in subdomains:
        if subdomain_obj["subdomain"] == subdomain:
            urls = subdomain_obj["urls"]
            # Urls Set
            for url_obj in urls:
                if url_obj["url"] == url:
                    try:
                        parameters = url_obj["parameters"]
                    except KeyError:
                        url_obj["parameters"] = []
                        doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
    for parameter in parameters_list:
        subdomains = doc["subdomains"]
        if not IsUrlParameter(client, dbname, collname, domain, subdomain, url, parameter)[1]:
            for subdomain_obj in subdomains:
                if subdomain_obj["subdomain"] == subdomain:
                    urls = subdomain_obj["urls"]
                    # Urls Set
                    for url_obj in urls:
                        if url_obj["url"] == url:
                            try:
                                parameters = url_obj["parameters"]
                            except KeyError:
                                url_obj["parameters"] = []
                            url_obj["parameters"].append({"parameter": parameter})
                            added_parameters.append(parameter)
                            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
    return added_parameters

# function RemoveUrlParameter to remove a url parameter from a collection(target) in a database and return the deleted url parameter object's _id and object itself on success
def RemoveUrlParameter(client, dbname, collname, domain, subdomain, url, parameter):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    _, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return "", []
    # Check if subdomain exists
    _, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        return "", []
    # Check if url exists
    _, urlexists = IsUrl(client, dbname, collname, domain, subdomain, url)
    if not urlexists:
        return "", []
    # Check if parameter exists
    _, parameterexists = IsUrlParameter(client, dbname, collname, domain, subdomain, url, parameter)
    if not parameterexists:
        return "", []

    # Get the document object
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            for url_obj in subdomain_obj["urls"]:
                if url_obj["url"] == url:
                    for parameter_obj in url_obj["parameters"]:
                        if parameter_obj["parameter"] == parameter:
                            url_obj["parameters"].remove(parameter_obj)
                            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
                            return parameter_obj, doc["_id"]
    return "", ""

# function ListDirectories to list all directories in a subdomain in a domain in a collection(target) in a database and return the list of directories
def ListDirectories(client, dbname, collname, domain, subdomain):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return "", []
    # Check if subdomain exists
    docs, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        return "", []

    # Get the list of directories - sample doc:
    # {
    #     "domain": "example.com",
    #     "subdomains": [
    #         {
    #             "subdomain": "www",
    #             "directories": [
    #                 {
    #                     "directory": "/about"
    #                 },
    #                 {
    #                     "directory": "/contact"
    #                 }
    #             ]
    #         }
    #     ]
    # }
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    directories_list = []
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                doc_directories = subdomain_obj["directories"]
            except KeyError:
                return docs, directories_list
            for directory_obj in subdomain_obj["directories"]:
                directories_list.append(directory_obj["directory"])
    return docs, directories_list

# function IsDirectory to check if a directory exists in a collection(target) in a database and return the result
def IsDirectory(client, dbname, collname, domain, subdomain, directory):
    docs, directories_list = ListDirectories(client, dbname, collname, domain, subdomain)
    if directory in directories_list:
        return docs, True
    else:
        return docs, False

# function AddDirectories to add mulitple directories to a collection(target) in a database and return the directory object's id on success
def AddDirectories(client, dbname, collname, domain, subdomain, directories):
    # Split directories by " "
    directories_list = re.split(r"\s+", directories)

    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Check if domain exists
    docs, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        # Add domain
        doc_id = AddDomain(client, dbname, collname, domain)
        doc = GetDomain(client, dbname, collname, domain)
    # Check if subdomain exists
    docs, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        # Add subdomain
        doc_id = AddSubdomain(client, dbname, collname, domain, subdomain)
        doc = GetDomain(client, dbname, collname, domain)

    # set the doc using GetDomain
    doc = GetDomain(client, dbname, collname, domain)

    # Directories should be added to the subdomain data be like:
    # {
    #     "domain": "example.com",
    #     "subdomains": [
    #         {
    #             "subdomain": "www",
    #             "directories": [
    #                 {
    #                     "directory": "/about"
    #                 },
    #                 {
    #                     "directory": "/contact"
    #                 }
    #             ]
    #         }
    #     ]
    # }
    # So directory should be added to where subdomain is equal to subdomain
    added_directories = []
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            try:
                doc_directories = subdomain_obj["directories"]
            except KeyError:
                subdomain_obj["directories"] = []
            for directory in directories_list:
                if not IsDirectory(client, dbname, collname, domain, subdomain, directory)[1]:
                    subdomain_obj["directories"].append({"directory": directory})
                    added_directories.append(directory)
            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
    return added_directories

# function RemoveDirectory to remove a directory from a collection(target) in a database and return the deleted directory object's _id and object itself on success
def RemoveDirectory(client, dbname, collname, domain, subdomain, directory):
    # Check if directory exists
    docs, directoryexists = IsDirectory(client, dbname, collname, domain, subdomain, directory)
    if not directoryexists:
        return "", ""
    # Get the document object
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    # Remove directory
    for directory_obj in doc["directories"]:
        if directory_obj["directory"] == directory:
            doc["directories"].remove(directory_obj)
            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
            return directory_obj, doc["_id"]
    return "", ""

# function ListFiles to list all files in a directory in a subdomain in a domain in a collection(target) in a database and return the list of files
def ListFiles(client, dbname, collname, domain, subdomain, directory):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    _, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return "", []
    # Check if subdomain exists
    _, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        return "", []
    # Check if directory exists
    _, directoryexists = IsDirectory(client, dbname, collname, domain, subdomain, directory)
    if not directoryexists:
        return "", []
    # Get the list of files - sample doc:
    # {
    #     "domain": "example.com",
    #     "subdomains": [
    #         {
    #             "subdomain": "www",
    #             "directories": [
    #                 {
    #                     "directory": "/about",
    #                     "files": [
    #                         {
    #                             "file": "index.html"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    files_list = []
    try:
        subdomains = doc["subdomains"]
    except KeyError:
        return "", []
    for subdomain_obj in subdomains:
        if subdomain_obj["subdomain"] == subdomain:
            try: 
                directories = subdomain_obj["directories"]
            except KeyError:
                return "", []
            for directory_obj in directories:
                if directory_obj["directory"] == directory:
                    try:
                        files = directory_obj["files"]
                    except KeyError:
                        return "", []
                    for file_obj in files:
                        if file_obj["file"] not in files_list:
                            files_list.append(file_obj["file"])
    return doc, files_list

# function IsFile to check if a file exists in a directory in a subdomain in a domain in a collection(target) in a database and return the result
def IsFile(client, dbname, collname, domain, subdomain, directory, file):
    docs, files_list = ListFiles(client, dbname, collname, domain, subdomain, directory)
    if file in files_list:
        return docs, True
    else:
        return docs, False

# function AddFiles to add files to a directory in a subdomain in a domain in a collection(target) in a database and return the list of added files
def AddFiles(client, dbname, collname, domain, subdomain, directory, files):
    # Split files by " "
    files_list = re.split(r"\s+", files)

    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Check if domain exists
    _, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        # Add domain
        _ = AddDomain(client, dbname, collname, domain)
    # Check if subdomain exists
    _, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        # Add subdomain
        _ = AddSubdomain(client, dbname, collname, domain, subdomain)
    # Check if directory exists
    _, directoryexists = IsDirectory(client, dbname, collname, domain, subdomain, directory)
    if not directoryexists:
        # Add directory
        _ = AddDirectories(client, dbname, collname, domain, subdomain, directory)

    # Set the document object
    doc = GetDomain(client, dbname, collname, domain)
    added_files = []

    # Files should be added inside a subdomain and inside a directory + handle duplicates + handle KeyErrors when subdomain["directories"] or directory["files"] doesn't exist
    subdomains = doc["subdomains"]
    for subdomain_obj in subdomains:
        if subdomain_obj["subdomain"] == subdomain:
            directories = subdomain_obj["directories"]
            # Directories Set
            for directory_obj in directories:
                if directory_obj["directory"] == directory:
                    try:
                        files = directory_obj["files"]
                    except KeyError:
                        directory_obj["files"] = []
                        doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
    for file in files_list:
        subdomains = doc["subdomains"]
        if not IsFile(client, dbname, collname, domain, subdomain, directory, file)[1]:
            for subdomain_obj in subdomains:
                if subdomain_obj["subdomain"] == subdomain:
                    directories = subdomain_obj["directories"]
                    # Directories Set
                    for directory_obj in directories:
                        if directory_obj["directory"] == directory:
                            files = directory_obj["files"]
                            directory_obj["files"].append({"file": file})
                            added_files.append(file)
                            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
    return added_files

# function RemoveFile to remove a file from a directory in a subdomain in a domain in a collection(target) in a database and return the file removed
def RemoveFile(client, dbname, collname, domain, subdomain, directory, file):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return "", []
    # Check if domain exists
    _, domainexists = IsDomain(client, dbname, collname, domain)
    if not domainexists:
        return "", []
    # Check if subdomain exists
    _, subdomainexists = IsSubdomain(client, dbname, collname, domain, subdomain)
    if not subdomainexists:
        return "", []
    # Check if directory exists
    _, directoryexists = IsDirectory(client, dbname, collname, domain, subdomain, directory)
    if not directoryexists:
        return "", []
    # Check if file exists
    _, fileexists = IsFile(client, dbname, collname, domain, subdomain, directory, file)
    if not fileexists:
        return "", []

    # Get the list of files - sample doc:
    # {
    #     "domain": "example.com",
    #     "subdomains": [
    #         {
    #             "subdomain": "www",
    #             "directories": [
    #                 {
    #                     "directory": "/about",
    #                     "files": [
    #                         {
    #                             "file": "index.html"
    #                         }
    #                     ]
    #                 }
    #             ]
    #         }
    #     ]
    # }
    doc = QueryDocument(client, dbname, collname, {"domain": domain})
    for subdomain_obj in doc["subdomains"]:
        if subdomain_obj["subdomain"] == subdomain:
            for directory_obj in subdomain_obj["directories"]:
                if directory_obj["directory"] == directory:
                    for file_obj in directory_obj["files"]:
                        if file_obj["file"] == file:
                            directory_obj["files"].remove(file_obj)
                            doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], doc)
                            return file_obj, doc["_id"]
    return "", ""

# function ListPart, gets client, dbname, collname and parts as *args and returns the members of the parts
def ListPart(client, dbname, collname, *args, **kwargs):
    seperator()
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    
    # if len of kwargs is 0, then return all the documents in the collection
    print("kwargs: ", kwargs)
    if len(kwargs) == 0:
        docs_ids = ListDocuments(client, dbname, collname)
        print("no kwargs found, returning all docs inside collection...")
        return docs_ids

    # print the first pair in kwargs, use NthKey function
    print("NthKey(kwargs, 0): ", NthKey(kwargs, 0))

    doc = QueryDocument(client, dbname, collname, NthKey(kwargs, 0))
    print("data after filter with kwargs[0]: ", doc)
    # if doc is empty then return None
    if not doc:
        return ""
    doc_id = doc["_id"]
    # shift kwargs 1 to the left
    kwargs = ShiftLeft(kwargs, 1)
    print("kwargs after shift: ", kwargs)

    # if len of args is 0, then return the document
    if len(args) == 0:
        return doc
    
    # iterate over the args and get the members of the parts in both args and kwargs
    for i, arg in enumerate(args):
        try:
            print("selecting part: ", arg, " from the document:", doc)
            doc = doc[arg]
            print("current doc after selection: ", doc)
        except KeyError as err:
            return ""
        except TypeError as err:
            return ""
        # if len of kwargs is 0, then return the doc
        print("kwargs: ", kwargs)
        if len(kwargs) == 0:
            print("kwargs is empty, returning doc: ", doc)
            return doc
        # if len of kwargs is not 0, then use kwargs[0] as query to find the document(e.g. {"subdomain": "sub1"})
        queryjson = Query(NthKey(kwargs, 0))
        try:
            doc = list(filter(Query(NthKey(kwargs, 0)).match, doc))[0]
        except IndexError as err:
            return ""
        print("data after filter with {} : {}".format(NthKey(kwargs, 0), doc))
        # doc, err = QueryDocument(client, dbname, collname, NthKey(kwargs, 0))
        if err:
            return ""
        # if doc is empty then return None
        if not doc:
            return ""
        # shift kwargs 1 to the left
        kwargs = ShiftLeft(kwargs, 1)
        print("kwargs after shift: ", kwargs)
    # return the doc
    return doc

# function GetInfo, gets client, dbname, collname, a json filter (as string, e.g. `{"domain": "domain1.com"}`) and parts as *args (all members of args are strings) and returns the members of the parts
def GetInfo(client, dbname, collname, filterjson=None, *args):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
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
    doc = QueryDocument(client, dbname, collname, filterjson)
    # if doc is empty then return None
    if not doc:
        raise Exception("No document found")
    
    # if len of args is 0, then return the document
    if len(args) == 0:
        return doc
    
    # From now on, we have a document and we need to get the members of the parts in args, so we use GetFromJson function to get the members of the parts in args
    doc = GetFromJson(doc, *args)
    return doc

# function ListTargetInfo_h1, gets client, dbname, collname and returns the list of target handles in the collection
def ListTargetInfo_h1(client, dbname, collname):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    # Iterate over the list of documents
    handles_list = []
    for doc_id in docs:
        # Get the document object
        doc = QueryDocument(client, dbname, collname, {"_id": doc_id})
        # In that json object select attributes->handle
        try:
            handle = doc["attributes"]["handle"]
        except KeyError:
            continue
        # Append handle to handles_list
        handles_list.append(handle)
    # Return handles_list
    return handles_list

# function IsTargetInfo_h1, gets client, dbname, collname and target_handle, iterates over the list of documents in the collection and returns true if target already exists
def IsTargetInfo_h1(client, dbname, collname, target_handle):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return False
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    # Iterate over the list of documents
    for doc in docs:
        # In that json object select attributes->handle
        try:
            handle = doc["attributes"]["handle"]
        except KeyError:
            continue
        # If handle is equal to target_handle then return True
        if handle == target_handle:
            return True
    # If not found then return False
    return False

# function AddTargetInfo_h1, gets client, dbname, collname and a json object and adds the json object to the collection if a document with the same handle doesn't exist, if it exists then it updates the document
def AddTargetInfo_h1(client, dbname, collname, jsonobj):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    
    jsonobj = json.loads(jsonobj)
    jsonobj_handle = jsonobj["attributes"]["handle"]
    
    # Iterate over the list of documents
    for doc_id in docs:
        # Get the document object
        doc = QueryDocument(client, dbname, collname, {"_id": doc_id})
        # In that json object select attributes->handle
        try:
            handle = doc["attributes"]["handle"]
        except KeyError:
            continue
        if handle == jsonobj_handle:
            new_doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], jsonobj)
            new_doc_id = new_doc["_id"]
            return new_doc_id
    # If not found then add the document
    new_doc_id = AddDocument(client, dbname, collname, jsonobj)
    return new_doc_id

# function GetTargetInfo_h1, gets client, dbname, collname and target_handle, iterates over the list of documents in the collection and returns the document with the same handle if found
def GetTargetInfo_h1(client, dbname, collname, target_handle):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    for doc in docs:
        # In that json object select attributes->handle
        try:
            handle = doc["attributes"]["handle"]
        except KeyError:
            continue
        # If handle is equal to target_handle then return the document
        if handle == target_handle:
            return doc
    # If not found then return None
    return ""

# function RemoveTargetInfo_h1, gets client, dbname, collname and target_handle, iterates over the list of documents in the collection and removes the document with the same handle if found
def RemoveTargetInfo_h1(client, dbname, collname, target_handle):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    # Iterate over the list of documents
    for doc_id in docs:
        # Get the document object
        doc = QueryDocument(client, dbname, collname, {"_id": doc_id})
        # In that json object select attributes->handle
        try:
            handle = doc["attributes"]["handle"]
        except KeyError:
            continue
        # If handle is equal to target_handle then remove the document
        if handle == target_handle:
            RemoveDocument(client, dbname, collname, doc["_id"])
            return doc["attributes"]["handle"]
    # If not found then return None
    return ""

# function ListTargetInfo_bc, gets client, dbname, collname and returns the list of target handles in the collection
def ListTargetInfo_bc(client, dbname, collname):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    # Iterate over the list of documents
    handles_list = []
    for doc_id in docs:
        # Get the document object
        doc = QueryDocument(client, dbname, collname, {"_id": doc_id})
        # In that json object select >code
        try:
            handle = doc["code"]
        except KeyError:
            continue
        # Append handle to handles_list
        handles_list.append(handle)
    # Return handles_list
    return handles_list

# function IsTargetInfo_bc, gets client, dbname, collname and target_handle, iterates over the list of documents in the collection and returns true if target already exists
def IsTargetInfo_bc(client, dbname, collname, target_handle):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return False
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    # Iterate over the list of documents
    for doc in docs:
        # In that json object select >code
        try:
            handle = doc["code"]
        except KeyError:
            continue
        # If handle is equal to target_handle then return True
        if handle == target_handle:
            return True
    # If not found then return False
    return False

# function AddTargetInfo_bc, gets client, dbname, collname and a json object and adds the json object to the collection if a document with the same handle doesn't exist, if it exists then it updates the document
def AddTargetInfo_bc(client, dbname, collname, jsonobj_addr):
    f = open(jsonobj_addr, "r")
    jsonobj = json.load(f)
    f.close()
    # remove the file
    os.remove(jsonobj_addr)
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        # Create collection
        CreateCollection(client, dbname, collname)
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    
    jsonobj_handle = jsonobj["code"]
    
    # Iterate over the list of documents
    for doc_id in docs:
        # Get the document object
        doc = QueryDocument(client, dbname, collname, {"_id": doc_id})
        # In that json object select attributes->handle
        try:
            handle = doc["code"]
        except KeyError:
            continue
        if handle == jsonobj_handle:
            new_doc = UpdateDocumentByID(client, dbname, collname, doc["_id"], jsonobj)
            new_doc_id = new_doc["_id"]
            return new_doc_id
    # If not found then add the document
    new_doc_id = AddDocument(client, dbname, collname, jsonobj)
    return new_doc_id

# function GetTargetInfo_bc, gets client, dbname, collname and target_handle, iterates over the list of documents in the collection and returns the document with the same handle if found
def GetTargetInfo_bc(client, dbname, collname, target_handle):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    db = client[dbname]
    coll = db[collname]
    docs = coll.find()
    for doc in docs:
        # In that json object select >code
        try:
            handle = doc["code"]
        except KeyError:
            continue
        # If handle is equal to target_handle then return the document
        if handle == target_handle:
            return doc
    # If not found then return None
    return ""

# function RemoveTargetInfo_bc, gets client, dbname, collname and target_handle, iterates over the list of documents in the collection and removes the document with the same handle if found
def RemoveTargetInfo_bc(client, dbname, collname, target_handle):
    # Check if collection exists
    collexists = IsCollection(client, dbname, collname)
    if not collexists:
        return ""
    # Get the list of documents
    docs = ListDocuments(client, dbname, collname)
    # Iterate over the list of documents
    for doc_id in docs:
        # Get the document object
        doc = QueryDocument(client, dbname, collname, {"_id": doc_id})
        # In that json object select >code
        try:
            handle = doc["code"]
        except KeyError:
            continue
        # If handle is equal to target_handle then remove the document
        if handle == target_handle:
            RemoveDocument(client, dbname, collname, doc["_id"])
            return doc["code"]
    # If not found then return None
    return ""

#