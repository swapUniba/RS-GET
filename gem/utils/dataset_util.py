import os



# Prende le componenti di Training e Test e modifica gli ID degli Item aggiungendo 10.000.
def createDisgiuntiBaseTest(dataset):

    edge_list_fB = 'gem/datasets/' + dataset + '/u1.base'
    sBase = ""
    with open(edge_list_fB, 'r') as brB:
        for line in brB:
    	    ln = line.strip().split()
    	    sBase = sBase + ln[0] + '\t' + repr( (int(ln[1])) + 10000 ) + '\t' + ln[2] + '\n'
    with open('gem/datasets/' + dataset + '/u1Disjointed.base', 'w') as bwB:
        bwB.write(sBase)

    edge_list_fT = 'gem/datasets/' + dataset + '/u1.test'
    sTest = ""
    with open(edge_list_fT, 'r') as brT:
        for line in brT:
    	    ln = line.strip().split()
    	    sTest = sTest + ln[0] + '\t' + repr( (int(ln[1])) + 10000 ) + '\t' + ln[2] + '\n'
    with open('gem/datasets/' + dataset + '/u1Disjointed.test', 'w') as bwT:
        bwT.write(sTest)



# Costruisce un file composto dalle relazioni "Utente-Item" prelevati dalle relazioni positive presenti nella componente originale.
def createLikeBase(dataset):

    stringBase = ""
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as brBase:
        for line in brBase:
            ln = line.strip().split()
            if (int(ln[2]) == 1):
                stringBase = stringBase + ln[0] + '\t' + ln[1] + '\n'

    with open('gem/datasets/' + dataset + '/u1LIKE.base', 'w') as bwBase:
        bwBase.write(stringBase)



# Costruisce un file composto dalle relazioni "Utente-Item" prelevati dalle relazioni positive presenti nella componente originale.
def createLikeTest(dataset):

    stringTest = ""
    with open('gem/datasets/' + dataset + '/u1.test', 'r') as brTest:
        for line in brTest:
            ln = line.strip().split()
            if (int(ln[2]) == 1):
                stringTest = stringTest + ln[0] + '\t' + ln[1] + '\n'

    with open('gem/datasets/' + dataset + '/u1LIKE.test', 'w') as bwTest:
        bwTest.write(stringTest)



# Costruisce dataset con ID compatti, considerando complessivamente gli ID presenti nel file di Training (.base) e di test (.test), (solo LIKE)
def constructIDCompactLike(dataset):

    listNodesBase = []
    with open('gem/datasets/' + dataset + '/u1LIKE.base', 'r') as brBase:
        for line in brBase:
            ln = line.strip().split()
            listNodesBase.append(int(ln[0]))
            listNodesBase.append(int(ln[1]))

    listNodesTest = []
    with open('gem/datasets/' + dataset + '/u1LIKE.test', 'r') as brTest:
        for line in brTest:
            ln = line.strip().split()
            listNodesTest.append(int(ln[0]))
            listNodesTest.append(int(ln[1]))

    listNodes = listNodesBase + listNodesTest
    listNodes = list(set(listNodes))
    listNodes.sort()

    print "Lista di tutti i nodi presenti in .base e .test:\n", listNodes

    stringBase = ""
    with open('gem/datasets/' + dataset + '/u1LIKE.base', 'r') as brBase:
        for line in brBase:
            ln = line.strip().split()
            stringBase = stringBase + repr(listNodes.index(int(ln[0]))) + '\t' + repr(listNodes.index(int(ln[1]))) + '\n'
    with open('gem/datasets/' + dataset + '/u1LIKECompact.base', 'w') as bwBase:
        bwBase.write(stringBase)
    bwBase.close()

    stringTest = ""
    with open('gem/datasets/' + dataset + '/u1LIKE.test', 'r') as brTest:
        for line in brTest:
            ln = line.strip().split()
            stringTest = stringTest + repr(listNodes.index(int(ln[0]))) + '\t' + repr(listNodes.index(int(ln[1]))) + '\n'
    with open('gem/datasets/' + dataset + '/u1LIKECompact.test', 'w') as bwTest:
        bwTest.write(stringTest)
    bwTest.close()



# Costruisce dataset con ID compatti considerando complessivamente sia gli ID presenti nel file di Training (.base) che in quello di test (.test), (sia LIKE, che DISLIKE).
def constructIDCompactLikeDislike(dataset):

    listNodesBase = []
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as brBase:
        for line in brBase:
            ln = line.strip().split()
            listNodesBase.append(int(ln[0]))
            listNodesBase.append(int(ln[1]))

    listNodesTest = []
    with open('gem/datasets/' + dataset + '/u1.test', 'r') as brTest:
        for line in brTest:
            ln = line.strip().split()
            listNodesTest.append(int(ln[0]))
            listNodesTest.append(int(ln[1]))

    listNodes = listNodesBase + listNodesTest
    listNodes = list(set(listNodes))
    listNodes.sort()

    print "Lista di tutti i nodi presenti in .base e .test:\n", listNodes

    stringBase = ""
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as brBase:
        for line in brBase:
            ln = line.strip().split()
            stringBase = stringBase + repr(listNodes.index(int(ln[0]))) + '\t' + repr(listNodes.index(int(ln[1]))) + '\t' + ln[2] + '\n'
    with open('gem/datasets/' + dataset + '/u1Compact.base', 'w') as bwBase:
        bwBase.write(stringBase)
    bwBase.close()

    stringTest = ""
    with open('gem/datasets/' + dataset + '/u1.test', 'r') as brTest:
        for line in brTest:
            ln = line.strip().split()
            stringTest = stringTest + repr(listNodes.index(int(ln[0]))) + '\t' + repr(listNodes.index(int(ln[1]))) + '\t' + ln[2] + '\n'
    with open('gem/datasets/' + dataset + '/u1Compact.test', 'w') as bwTest:
        bwTest.write(stringTest)
    bwTest.close()



# Crea un solo file composto sia dalla componente di Training che da quella di Test, (solo LIKE)
def createBaseTestInOne(dataset):

    stringBase = ""
    with open('gem/datasets/' + dataset + '/u1LIKECompact.base', 'r') as brBase:
        for line in brBase:
            ln = line.strip().split()
            stringBase = stringBase + ln[0] + '\t' + ln[1] + '\n'

    stringTest = ""
    with open('gem/datasets/' + dataset + '/u1LIKECompact.test', 'r') as brTest:
        for line in brTest:
            ln = line.strip().split()
            stringTest = stringTest + ln[0] + '\t' + ln[1] + '\n'

    stringAll = stringBase + stringTest
    with open('gem/datasets/' + dataset + '/u1LIKECompact.edgelist', 'w') as bwAll:
        bwAll.write(stringAll)



# Crea un nuovo file composto sia dalla componente di Training che da quella di Test.
def createOneDatasetWithAllRatings(dataset):

    bw = open('gem/datasets/' + dataset + '/u1All.edgelist', 'w')

    with open('gem/datasets/' + dataset + '/u1.base', 'r') as brB:
        for line in brB:
            ln = line.strip().split()
            bw.write(ln[0] + "\t" + ln[1] + "\n")
    brB.close()

    with open('gem/datasets/' + dataset + '/u1.test', 'r') as brT:
        for line in brT:
            ln = line.strip().split()
            bw.write(ln[0] + "\t" + ln[1] + "\n")
    brT.close()

    bw.close()



# Costruisce dataset con ID compatti, considerando complessivamente il file di Training (u1.base), il file di test (u1.test) e il file u1LIKEItemObject.base
def constructIDCompactBaseTestItemObject(dataset):

    listAllNodes = []
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as brB:
        for line in brB:
            ln = line.strip().split()
            listAllNodes.append(int(ln[0]))
            listAllNodes.append(int(ln[1]))
    brB.close()

    with open('gem/datasets/' + dataset + '/u1.test', 'r') as brT:
        for line in brT:
            ln = line.strip().split()
            listAllNodes.append(int(ln[0]))
            listAllNodes.append(int(ln[1]))
    brT.close()

    with open('gem/datasets/' + dataset + 'ItemObject/u1LIKEItemObject.base', 'r') as brIO:
        for line in brIO:
            ln = line.strip().split()
            listAllNodes.append(int(ln[0]))
            listAllNodes.append(int(ln[1]))
    brIO.close()

    listAllNodes = list(set(listAllNodes))
    listAllNodes.sort()

    #print "Lista di tutti i nodi presenti:", listAllNodes

    bwBase = open('gem/datasets/' + dataset + '/u1Compact.base', 'w')
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as brBase:
        for line in brBase:
            ln = line.strip().split()
            bwBase.write( repr(listAllNodes.index(int(ln[0]))) + '\t' + repr(listAllNodes.index(int(ln[1]))) + '\t' + ln[2] + '\n' )
    brBase.close()
    bwBase.close()

    bwTest = open('gem/datasets/' + dataset + '/u1Compact.test', 'w')
    with open('gem/datasets/' + dataset + '/u1.test', 'r') as brTest:
        for line in brTest:
            ln = line.strip().split()
            bwTest.write( repr(listAllNodes.index(int(ln[0]))) + '\t' + repr(listAllNodes.index(int(ln[1]))) + '\t' + ln[2] + '\n' )
    brTest.close()
    bwTest.close()

    bwItemObject = open('gem/datasets/' + dataset + 'ItemObject/u1LIKEItemObjectCompact.base', 'w')
    with open('gem/datasets/' + dataset + 'ItemObject/u1LIKEItemObject.base', 'r') as brItemObject:
        for line in brItemObject:
            ln = line.strip().split()
            bwItemObject.write( repr(listAllNodes.index(int(ln[0]))) + '\t' + repr(listAllNodes.index(int(ln[1]))) + '\n' )
    brItemObject.close()
    bwItemObject.close()



# Crea un nuovo file composto sia dalle relazioni "Utente-Item" che "Item-Object".
def concatenateUtenteItem_ItemObject(dataset):
    if not os.path.exists("gem/datasets/" + dataset + "UserItemObject"):
        os.makedirs("gem/datasets/" + dataset + "UserItemObject")
    bw = open("gem/datasets/" + dataset + "UserItemObject/u1LIKEUserItemObject.base", 'w')

    with open("gem/datasets/" + dataset + "/u1LIKE.base", 'r') as br1:
        for line in br1:
            bw.write(line)
    br1.close()

    with open("gem/datasets/" + dataset + "ItemObject/u1LIKEItemObject.base", 'r') as br2:
        for line in br2:
            bw.write(line)
    br2.close()

    bw.close()
