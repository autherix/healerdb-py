import inspect
from pymongo import MongoClient
from rich import print
from mod_utils import *
from mongoquery import Query, QueryError

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
        # Find the updated document
        doc = coll.find_one({"_id": doc_id})
        return doc, None
    except Exception as err:
        return None, err

# function ListDomains to list all domains in a collection(target) in a database and return the list of domains and error
def ListDomains(client, dbname, collname):
    try:
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
    except Exception as err:
        return None, None, err

# function IsDomain to check if a domain exists in a collection(target) in a database and return the result and error
def IsDomain(client, dbname, collname, domain):
    try:
        docs, domains_list, err = ListDomains(client, dbname, collname)
        if err:
            return None, None, err
        if domain in domains_list:
            return docs, True, None
        else:
            return docs, False, None
    except Exception as err:
        return None, None, err

# function AddDomain to add a domain to a collection(target) in a database and return the domain object's id on success and error
def AddDomain(client, dbname, collname, domain):
    try:
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
    except Exception as err:
        return None, err

# function RemoveDomain to remove one domain from a collection(target) in a database and return the deleted domain object's _id and object itself on success and error
def RemoveDomain(client, dbname, collname, domain):
    try:
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
    except Exception as err:
        return None, None, err

# function ListSubdomains to list all subdomains in a collection(target) in a database and return the list of subdomains and error
def ListSubdomains(client, dbname, collname, domain):
    try:
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
    except Exception as err:
        return None, None, err

# function IsSubdomain to check if a subdomain exists in a collection(target) in a database and return the result and error
def IsSubdomain(client, dbname, collname, domain, subdomain):
    try:
        docs, subdomains_list, err = ListSubdomains(client, dbname, collname, domain)
        if err:
            return None, None, err
        if subdomain in subdomains_list:
            return docs, True, None
        else:
            return docs, False, None
    except Exception as err:
        return None, None, err

# function AddSubdomain to add a subdomain to a collection(target) in a database and return the subdomain object's id on success and error
def AddSubdomain(client, dbname, collname, domain, subdomain):
    try:
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
    except Exception as err:
        return None, None, err

# function RemoveSubdomain to remove one subdomain from a collection(target) in a database and return the deleted subdomain object's _id and object itself on success and error
def RemoveSubdomain(client, dbname, collname, domain, subdomain):
    try:
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
    except Exception as err:
        return None, None, err

# Function to list all nestedsubdomains in a collection(target) in a database and return the list of nestedsubdomains and error
def ListNestedSubdomains(client, dbname, collname, domain, subdomain):
    try:
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
    except Exception as err:
        return None, None, err

# function IsNestedSubdomain to check if a nestedsubdomain exists in a collection(target) in a database and return the result and error
def IsNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    try:
        docs, nestedsubdomains_list, err = ListNestedSubdomains(client, dbname, collname, domain, subdomain)
        if err:
            return None, None, err
        if nestedsubdomain in nestedsubdomains_list:
            return docs, True, None
        else:
            return docs, False, None
    except Exception as err:
        return None, None, err
    
# function AddNestedSubdomain to add a nestedsubdomain to a collection(target) in a database and return the nestedsubdomain object's id on success and error
def AddNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    try:
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
    except Exception as err:
        return None, None, err

# function RemoveNestedSubdomain to remove one nestedsubdomain from a collection(target) in a database and return the deleted nestedsubdomain object's _id and object itself on success and error
def RemoveNestedSubdomain(client, dbname, collname, domain, subdomain, nestedsubdomain):
    try:
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
    except Exception as err:
        return None, None, err

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
    try:
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
    except Exception as err:
        return None, err

# function SetInfo, gets client, dbname, collname, data as json string, a json filter (as string, e.g. `{"domain": "domain1.com"}`) and parts as *args (all members of args are strings), writes the data to the members of the parts and returns the members of the parts and error
def NC_SetInfo(client, dbname, collname, data, init_query, *args):
    try:
        # Check if collection exists
        collexists, err = IsCollection(client, dbname, collname)
        if err:
            return None, err
        if not collexists:
            return None, Exception("Collection does not exist")

        try:
            # Convert init_query to json if it is not empty
            if init_query:
                init_query = json.loads(init_query)
        except Exception as err:
            return None, Exception("Cannot convert init_query to json")
        
        # If init_query is provided
        if init_query:
            print("init_query is provided")
            # Get the document object
            doc, err = QueryDocument(client, dbname, collname, init_query)
            if err:
                return None, err
            print("found doc: ", doc)
            # if doc is empty then return None
            if not doc:
                return None, Exception("No document found with the provided initial query")
            
            # Now we have one document, so we pass it to SetInJson function to set the data in the members of the parts in args
            newdoc, err = SetInJson(doc, data, *args)
            if err:
                return None, err
            print("newdoc from SetInJson: ", newdoc)
            # Update the document
            doc, err = UpdateDocument(client, dbname, collname, doc["_id"], newdoc)
            if err:
                return None, err
            print("updated doc: ", doc)
            return doc, None
        else:
            # List all the documents in the collection
            docs_ids, err = ListDocuments(client, dbname, collname)
            if err:
                return None, err
            print("docs_ids: ", docs_ids)
            # if docs_ids is empty then return None
            if not docs_ids:
                print("No documents found in the collection")
                return None, Exception("No documents found in the collection")
            # Iterate over the documents ids
            for doc_id in docs_ids:
                # Now we have a document id, so we pass it to SetInJson function to set the data in the members of the parts in args
                newdoc, err = SetInJson(doc_id, data, *args)
                if err:
                    return None, err
                # Update the document
                doc, err = UpdateDocument(client, dbname, collname, doc["_id"], newdoc)
                if err:
                    return None, err
            return docs_ids, None
    except Exception as err:
        return None, err

