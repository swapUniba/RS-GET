from SPARQLWrapper import SPARQLWrapper, JSON
import time
import os



# Esegue la Query per restituire il predicato e l'oggetto, a partire dal soggetto della tripla RDF.
def returnResults(u):
    query = """ SELECT ?p ?o
                WHERE { """ + "<" + u + ">" + " ?p ?o } "
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results



# Metodo che si occupa dell'esecuzione della Query per ottenere il predicato e l'oggetto, ed effettua della serializzazione dei risultati includendo anche il soggetto.
def obtainSubjectPredicateObject(dataset):

    lItems = []
    lUri = []
    nRighe = 0

    with open("gem/mappings/" + dataset + "_2DBpedia-1.2.tsv", 'r') as br:
        for line in br:
            ln = line.strip().split('\t')
            lItems.append(ln[0])
            lUri.append(ln[2])
            nRighe = nRighe + 1
    br.close()

    if ( (lItems.__len__() == lUri.__len__()) & (lItems.__len__() == nRighe) ):
        print "OK"
        n = lItems.__len__()
    else:
        exit()

    bw = open("gem/mappings/" + dataset + "_2DBpedia-1.2-ITEM-SUBJECT-PREDICATE-OBJECT.tsv", 'w')

    for i in range(0, n):
        print lUri[i]
        try:
            r = returnResults(lUri[i])
        except Exception:
            try:
                time.sleep(5)
                r = returnResults(lUri[i])
            except Exception:
                time.sleep(30)
                r = returnResults(lUri[i])

        for result in r["results"]["bindings"]:
            type = result["o"]["type"]
            if type == "uri":
                s = lItems[i] + '\t'+ lUri[i] + '\t' + result["p"]["value"] + '\t' + result["o"]["value"] + '\n'
                bw.write(s.encode("utf-8"))

    bw.close()



# Metodo che si occupa della trasformazione degli oggetti ottenuti dalla query in ID univoci, e della loro serializzazione;
# inoltre, aggiunge 10.000 agli ID item per farli corrispondere agli ID item presenti nei dataset ID utente -> ID item.
def createIDfromObjectUri(dataset):

    lItems = []
    lObjects = []

    with open("gem/mappings/" + dataset + "_2DBpedia-1.2-ITEM-SUBJECT-PREDICATE-OBJECT.tsv", 'r') as br:
        for line in br:
            ln = line.strip().split('\t')
            lItems.append(int(ln[0]))
            lObjects.append(ln[3])
    br.close()

    idMaxItem = (int(max(lItems))) + 10000

    lObjects = list(set(lObjects))
    lObjects.sort()

    bw = open("gem/mappings/" + dataset + "_2DBpedia-1.2-ITEM-OBJECT(ID).tsv", 'w')

    with open("gem/mappings/" + dataset + "_2DBpedia-1.2-ITEM-SUBJECT-PREDICATE-OBJECT.tsv", 'r') as br:
        for line in br:
            ln = line.strip().split('\t')
            bw.write(repr(int(ln[0]) + 10000) + '\t')   # Permette di disgiungere gli insiemi degli utenti ed degli item
            bw.write(repr((int(lObjects.index(ln[3]))) + idMaxItem + 1000) + '\n')

    bw.close()
    br.close()



# Metodo che si occupa dell'eliminazione delle coppie ripetute piu' volte nel file contenente la lista degli archi (ID-Item -> ID-Oggetto).
def deleteNotUniquePairs(dataset):

    lCoppieOrig = []
    with open("gem/mappings/" + dataset + "_2DBpedia-1.2-ITEM-OBJECT(ID).tsv", 'r') as br:
        for line in br:
            lCoppieOrig.append(line)
    br.close()

    lCoppieUniche = []
    for c in lCoppieOrig:
        if c not in lCoppieUniche:
            lCoppieUniche.append(c)

    with open("gem/mappings/" + dataset + "_u1LIKEItemObjectAll.base", 'w') as bw:
        for coppia in lCoppieUniche:
            bw.write(coppia)
    bw.close()



# Metodo che si occupa dell'eliminazione delle coppie estratte, in cui l'ID item non e' presente nel dataset originale.
def deleteRelations(dataset):

    lItemsConsiderare = []
    with open("gem/datasets/" + dataset + "/u1LIKE.base", 'r') as br:
        for line in br:
            ln = line.strip().split('\t')
            lItemsConsiderare.append(int(ln[1]))
    br.close()
    lItemsConsiderare = list(set(lItemsConsiderare))

    lCoppieEstratte = []
    with open("gem/mappings/" + dataset + "_u1LIKEItemObjectAll.base", 'r') as br:
        for line in br:
            lCoppieEstratte.append(line)
    br.close()

    lCoppieInserire = []
    for c in lCoppieEstratte:
        l = c.split('\t')
        print l[0]
        if (int(l[0])) in lItemsConsiderare:
            lCoppieInserire.append(c)

    if not os.path.exists("gem/datasets/" + dataset + "ItemObject"):
        os.makedirs("gem/datasets/" + dataset + "ItemObject")
    with open("gem/datasets/" + dataset + "ItemObject/u1LIKEItemObject.base", 'w') as bw:
        for coppia in lCoppieInserire:
            bw.write(coppia)
    bw.close()
