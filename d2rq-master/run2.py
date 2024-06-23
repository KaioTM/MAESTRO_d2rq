import os
import os.path
from franz.openrdf.connect import ag_connect
from franz.openrdf.rio.rdfformat import RDFFormat

os.system("/home/vboxuser/ag8.1.1/bin/agraph-control --config /home/vboxuser/ag8.1.1/lib/agraph.cfg stop"  )
os.system("/home/vboxuser/ag8.1.1/bin/agraph-control --config /home/vboxuser/ag8.1.1/lib/agraph.cfg start"  )

with ag_connect('dfanalyzer', host='http://127.0.0.1', port='10035',
                user='super', password='12345') as conn:
    print (conn.size())
    

# We assume that our data files live in this directory.
DATA_DIR = 'data'
path1 = os.path.join(DATA_DIR, '/home/vboxuser/Desktop/MAESTRO-main_v3/d2rq-master/dump.nt')
context = conn.createURI("file:///home/vboxuser/Desktop/MAESTRO-main_v3/d2rq-master/dump.nt#")

conn.add(path1, base=None, format=RDFFormat.NTRIPLES, contexts=None)

print('Kennedy triples (default graph): {count}'.format(
      count=conn.size('null')))
