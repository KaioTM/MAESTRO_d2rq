
def createMetadata(onto, metadataType, metadata):
    met = onto.Metadata(metadata)
    met.is_a.append(metadataType)
    return met

def addMetadata(onto, program, metadata):
    program.hasMetadata.append(metadata)
