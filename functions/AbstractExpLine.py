from pyvis.network import Network
import networkx as nx
from owlready2 import *

def verify_relation_att(rel, aas, net):
    result = []
    for att in rel.composedBy:
        for aa in aas:
            for in_relation in aa.hasInputRelation:
                if att in in_relation.composedBy:
                    # print(att, " da relacao ", rel, " pertence a ", in_relation)
                    # net.add_edge(rel, in_relation, weight=5, shape="square", label="shareAtt", color="black")
                    # return [rel.name, in_relation.name, att.name]
                    net.add_node(rel.name, title=rel.composedBy, group=2, shape="box", color="#FCF3CF")
                    net.add_node(in_relation.name, title=str(in_relation.composedBy), group=2, shape="box", color="#FCF3CF")
                    # net.add_edge(rel.name, in_relation.name, width=2, label="Share Attribute", color="black", title=att.name)
                    # print(in_relation.composedBy)


def showExpLine():
    ontoexpline = get_ontology("ontologies/ontoexpline.owl").load()

    nx_graph = nx.cycle_graph(4, create_using=None)

    exp_line_relations = ontoexpline.search(type=ontoexpline.Relation)
    exp_line_att = ontoexpline.search(type=ontoexpline.Attribute)
    exp_line_aa = ontoexpline.search(type=ontoexpline.Abstract_activity)

    net = Network("90%", "50%", directed=True, layout=True, heading="Experiment Line")


    for aa in exp_line_aa:
        color_node_aa="#95C0F9"
        caption=". Profile: Mandatory."
        if ontoexpline.Optional in aa.is_a:
            color_node_aa = "#F1948A"
            caption=". Profile: Optional."
        elif ((ontoexpline.Mandatory in aa.is_a) and ontoexpline.Variant in aa.is_a):
            color_node_aa = "#D4EFDF"
            caption =". Profile: Mandatory and Variant."

        net.add_node(str(aa.name), size=20, title= aa.name + caption, group=2, shape="box", color=color_node_aa, borderWidthSelected="3")
        for rel in exp_line_relations:

            if (rel in aa.hasInputRelation):
                net.add_node(str(rel.name), title=str(rel.composedBy), group=2, shape="box", color="#FCF3CF")
                net.add_edge(aa.name, rel.name, weight=50, shape="square", label="hasInputRelation", color="black")

            if (rel in aa.hasOutputRelation):
                net.add_node(str(rel.name), title=str(rel.composedBy), group=2, shape="box", color="#FCF3CF")
                net.add_edge(aa.name, rel.name, weight=5, shape="text", label="hasOutputRelation", color="black")

                verify = verify_relation_att(rel, exp_line_aa, net)

    # net.show_buttons(filter_=['physics'])
    net.show("visualizations/abstractVisualization.html")