def domainOperation(ontoexpline, operation):
    classSearch = ontoexpline.search(iri = "*"+operation)
    for item in classSearch:
        return item