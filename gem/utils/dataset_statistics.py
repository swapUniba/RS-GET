# Restituisce il numero di Utenti presenti in un dataset composto da relazioni del tipo "Utente-Item-Voto"
def numberUsers(dataset):

    lUsers = []
    #with open('gem/datasets/' + dataset + '/u1.test', 'r') as br:
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as br:
        for line in br:
    	    ln = line.strip().split()
    	    lUsers.append(int(ln[0]))
    lUsers = list(set(lUsers))  # Elimina i doppioni dalla lista
    lUsers.sort()  # Ordina la lista che contiene tutti gli ID contenuti nel Grafo originale

    return lUsers.__len__()



# Restituisce il numero di Item presenti in un dataset composto da relazioni del tipo "Utente-Item-Voto"
def numberItems(dataset):
    lItems = []
    #with open('gem/datasets/' + dataset + '/u1.test', 'r') as br:
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as br:
        for line in br:
            ln = line.strip().split()
            lItems.append(int(ln[1]))
    lItems = list(set(lItems))  # Elimina i doppioni dalla lista
    lItems.sort()  # Ordina la lista che contiene tutti gli ID contenuti nel Grafo originale

    return lItems.__len__()


# Restituisce il numero di utenti presenti complessivamente nelle componenti di Training e Test di un dataset composto da relazioni del tipo "Utente-Item-Voto".
def numberUsersBaseAndTest(dataset):
    lUsers = []
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as br1:
        for line in br1:
            ln = line.strip().split()
            lUsers.append(int(ln[0]))
    br1.close()

    with open('gem/datasets/' + dataset + '/u1.test', 'r') as br2:
        for line in br2:
            ln = line.strip().split()
            lUsers.append(int(ln[0]))
    br2.close()

    lUsers = list(set(lUsers))  # Elimina i doppioni dalla lista
    lUsers.sort()  # Ordina la lista che contiene tutti gli ID contenuti nel Grafo originale

    return lUsers.__len__()


# Restituisce il numero di item presenti complessivamente nelle componenti di Training e Test di un dataset composto da relazioni del tipo "Utente-Item-Voto".
def numberItemsBaseAndTest(dataset):
    lItems = []
    with open('gem/datasets/' + dataset + '/u1.base', 'r') as br1:
        for line in br1:
            ln = line.strip().split()
            lItems.append(int(ln[1]))
    br1.close()

    with open('gem/datasets/' + dataset + '/u1.test', 'r') as br2:
        for line in br2:
            ln = line.strip().split()
            lItems.append(int(ln[1]))
    br2.close()

    lItems = list(set(lItems))  # Elimina i doppioni dalla lista
    lItems.sort()  # Ordina la lista che contiene tutti gli ID contenuti nel Grafo originale

    return lItems.__len__()


# Restituisce il numero di voti positivi presenti in un dataset composto da relazioni del tipo "Utente-Item-Voto".
def numberPositiveRatings(dataset):

    nVotiPositivi = 0
    #with open('gem/datasets/' + dataset + '/u1.base', 'r') as br:
    with open('gem/datasets/' + dataset + '/u1.test', 'r') as br:
        for line in br:
    	    ln = line.strip().split()
    	    if (int(ln[2]) == 1):
                nVotiPositivi = nVotiPositivi + 1

    return nVotiPositivi


# Restituisce il numero di voti negativi presenti in un dataset composto da relazioni del tipo "Utente-Item-Voto".
def numberNegativeRatings(dataset):

    nVotiNegativi = 0
    #with open('gem/datasets/' + dataset + '/u1.base', 'r') as br:
    with open('gem/datasets/' + dataset + '/u1.test', 'r') as br:
        for line in br:
    	    ln = line.strip().split()
    	    if (int(ln[2]) == 0):
                nVotiNegativi = nVotiNegativi + 1

    return nVotiNegativi



# Restituisce il numero di oggetti presenti in un dataset composto da relazioni del tipo "Item-Oggetto".
def numberProperties(dataset):

    lObjects = []
    with open('gem/datasets/' + dataset + "/u1LIKEItemObject.base", 'r') as br:
        for line in br:
            ln = line.strip().split('\t')
            lObjects.append(int(ln[1]))
    br.close()
    lObjects = list(set(lObjects))

    return lObjects.__len__()
