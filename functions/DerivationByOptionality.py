import json

from pyvis.network import Network

from sources.TemplateExecution import createTemplate

def searchPrograms(wf):
    net = Network("90%", "50%", directed=True, layout=True, heading="Abstract Workflow")
    color_node_aa = "#95C0F9"

    for aa in wf:
        # print(aa[0].executedBy)
        for program in aa[0].executedBy:
            print(program)
        # for program in aa[0].executedBy:
            # print(program.name, program.hasInPort, program.hasOutPort)

def abstractDerivationByOptionality(ontoexpline):
    aa = ontoexpline.search(type= ontoexpline.Mandatory) #conjunto de atividades obrigatórias
    opt = ontoexpline.search(is_a= ontoexpline.Optional) #conjunto de atividades opcionais
    rel = ontoexpline.search(type = ontoexpline.Relation) #conjunto de relações

    abs_wf = []

    for activity in aa:
        # print("'activity':","'",activity.name,"'")
        abs_act = []
        abs_act.append(activity)

        #identificando relações opcionais
        for aa_opt in opt:
            for relation_opt in aa_opt.hasOutputRelation:
                if relation_opt in activity.hasInputRelation:
                    rel.remove(relation_opt) #removendo relações opcionais

        #identificando relações de e/s de cada atividade
        in_rel = []
        out_rel = []

        for relation in rel:
            if (relation in activity.hasInputRelation):
                # print("'input':","'",relation,"'")
                in_rel.append(relation)
            elif(relation in activity.hasOutputRelation):
                # print("'output':","'",relation,"'")
                out_rel.append(relation)

        abs_act.append(in_rel)
        abs_act.append(out_rel)
        abs_wf.append(abs_act)

        # print(abs_wf)

    searchPrograms(abs_wf)

