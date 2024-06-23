## Script para executar a traduçao das tabelas do dfanalyzer para o formato RDF Triplestore. Sera criado um arquivo .ttl e apos um arquivo .nt ##
import os
os.system("./generate-mapping -o dfanalyzer.ttl --skip-tables public.iact_sub_tree,public.iact_tree_gen,public.oact_sub_tree,public.oact_tree_gen -u monetdb -p monetdb jdbc:monetdb://localhost/dataflow_analyzer"  )
os.system("./dump-rdf -o dump.nt dfanalyzer.ttl" )

