import os

from functions.Metadata import createMetadata, addMetadata


def createActivityTemplate(ontoexpline, activity):
    print("|*** Creating template (py file) to: ", activity, " activity. Executing: ", os.path.basename(__file__)+"\n")
    f = open("sources/activities/act_"+activity+".py", "w")
    f.close()
    source = "sources/activities/act_"+activity+".py"
    return source


def createActivity(ontoexpline, name, domainOperation, inRelations, outRelations, optional, implementers, first):
    for program in implementers:
        if (domainOperation in program.is_a):
            activity = ontoexpline.Abstract_activity(name)
            activity.is_a.append(domainOperation)
            activity.hasInputRelation = inRelations
            activity.hasOutputRelation = outRelations
            activity.executedBy.append(program)
            program.implements.append(activity)
            act = createMetadata(ontoexpline, ontoexpline.Configuration_Parameter, "--act")
            addMetadata(ontoexpline, program, act)

            if (optional == True):
                activity.is_a.append(ontoexpline.Optional)
            else:
                activity.is_a.append(ontoexpline.Mandatory)
            if(first == True):
                activity.is_a.append(ontoexpline.First)
        else:
            print("|*** Activity e ", program," possuem tipos domínio incompatíveis!")

    for r in inRelations:
        r.consumedBy.append(activity)
    for r_out in outRelations:
        r_out.generatedBy.append(activity)

    print("|*** Creating Activity: ", activity.name, ". In:", os.path.basename(__file__))

    if (len(implementers) > 1):
        activity.is_a.append(ontoexpline.Variant)

    source = createActivityTemplate(ontoexpline, name)
    source_url = createMetadata(ontoexpline, ontoexpline.Url, source)
    addMetadata(ontoexpline, activity, source_url)

    print("***** source: ", source)
    # activity.hasTemplate(source)
    return activity