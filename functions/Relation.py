def createRelation(onto, name):
    relation = onto.Relation(name)
    return relation

def associateRelationAtt(relation, attributes):
    """[função utilizada para associar programas em portas]
            Arguments:
                relation {[relation object]} -- [instancia relation definido na ontologia]
                attributes {[attribute object list ]} -- [lista de instâncias do tipo attribute]
            """
    if attributes:
        relation.composedBy = attributes
    else:
        print("|*** Lista de atributos vazia!")
        return exit()