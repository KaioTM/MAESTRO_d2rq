import os
from franz.openrdf.sail.allegrographserver import AllegroGraphServer

AGRAPH_HOST = "http://127.0.0.1"
AGRAPH_PORT = int(os.environ.get('AGRAPH_PORT', '10035'))
AGRAPH_USER = "super"
AGRAPH_PASSWORD = "12345"



print("Connecting to AllegroGraph server --",
      "host:'%s' port:%s" % (AGRAPH_HOST, AGRAPH_PORT))
server = AllegroGraphServer(AGRAPH_HOST, AGRAPH_PORT,
                            AGRAPH_USER, AGRAPH_PASSWORD)
print("Available catalogs:")
for cat_name in server.listCatalogs():
    if cat_name is None:
        print('  - <root catalog>')
    else:
        print('  - ' + str(cat_name))
        
        catalog = server.openCatalog('')
print("Available repositories in catalog '%s':" % catalog.getName())
for repo_name in catalog.listRepositories():
    print('  - ' + repo_name)
