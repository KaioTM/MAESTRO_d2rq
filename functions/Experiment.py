#Essa função define e instancia um individuo que é usado como id do Dataflow da dfanalyzer.
#atividades e programas são relaciodos a essa instancia
def createExperiment(ontoexpline, experimentId):
    experiment = ontoexpline.Workflow(experimentId)
    return experiment