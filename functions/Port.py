def createPort(onto, name):
    port = onto.Port(name)
    return port
def associatePortAtt(port, att):
    port.wasAssociatedWith.append(att)
    att.wasAssociatedWith.append(port)