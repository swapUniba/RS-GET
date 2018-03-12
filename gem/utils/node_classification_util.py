import numpy as np



# Restituisce la lista degli item graditi dall'utente con i corrispondenti Embedding.
def collectPositiveExamples(userID, emb, f_edge_list):

    # Per prendere gli ID degli Item graditi dall'Utente, dal file contenente la lista degli archi
    lItems = []
    with open(f_edge_list, 'r') as br:
        for line in br:
            ln = line.strip().split()
            if ((userID == int(ln[0])) & (int(ln[2]) == 1)):   # Se l'ID dell'Utente corrisponde a quello inserito, allora memorizza l'item
                lItems.append(int(ln[1]))
    userPositiveExamples = np.asarray(lItems, dtype=int)

    # Per prendere gli Embedding dei nodi Item graditi dall'utente
    lEmbItems = []
    for uPEx in userPositiveExamples:   # Popola la lista che conterra' gli embedding degli Item graditi dall'Utente
        lEmbItems.append(emb[uPEx])
    userPositiveExamples_embs = np.asarray(lEmbItems, dtype=float)

    return userPositiveExamples, userPositiveExamples_embs



# Restituisce la lista degli item NON graditi dall'utente con i corrispondenti Embedding.
def collectNegativeExamples(userID, emb, f_edge_list):
    lItems = []
    with open(f_edge_list, 'r') as br:
        for line in br:
            ln = line.strip().split()
            if ((userID == int(ln[0])) & (int(ln[2]) == 0)):   # Se l'ID dell'Utente corrisponde a quello inserito, allora memorizza l'item
                lItems.append(int(ln[1]))
    userNegativeExamples = np.asarray(lItems, dtype=int)

    # Per prendere gli Embedding dei nodi Item NON graditi dall'utente
    lEmbItems = []
    for uPEx in userNegativeExamples:   # Popola la lista che conterra' gli embedding degli Item NON graditi dall'Utente
        lEmbItems.append(emb[uPEx])
    userNegativeExamples_embs = np.asarray(lEmbItems, dtype=float)

    return userNegativeExamples, userNegativeExamples_embs



# Restituisce la lista degli item dell'utente da testare con i corrispondenti Embedding.
def collectItemsTest(userID, emb, f_edge_list):
    lItems = []
    with open(f_edge_list, 'r') as br:
        for line in br:
            ln = line.strip().split()
            if (userID == int(ln[0])):  # Se l'ID dell'Utente corrisponde a quello inserito, allora memorizza l'item
                lItems.append(int(ln[1]))
    userTestItems = np.asarray(lItems, dtype=int)

    # Per prendere gli Embedding dei nodi Item da testare dell'Utente inserito
    lEmbItems = []
    for uPEx in userTestItems:  # Popola la lista che conterra' gli embedding dei nodi Item da testare dell'Utente inserito
        try:
            lEmbItems.append(emb[uPEx])
        except:
            lEmbItems.append(np.zeros(emb.shape[1]))
    userTestItems_embs = np.asarray(lEmbItems, dtype=float)

    return userTestItems, userTestItems_embs



# Restituisce la lista di utenti presenti nel file dato in input, del tipo "Utente-Item".
def listUsers(f_edge_list):

    lUsers = []
    with open(f_edge_list, 'r') as br:
        for line in br:
            ln = line.strip().split()
            lUsers.append(int(ln[0]))   # Aggiunge alla lista l'ID dell'Utente

    lUsers = list(set(lUsers))  # Elimina i doppioni dalla lista
    return lUsers



# Restituisce la lista di voti di un utente, presenti nel file dato in input del tipo "Utente-Item-Voto".
def listRatings(userID, f_edge_list):

    lVoti = []
    with open(f_edge_list, 'r') as br:
        for line in br:
            ln = line.strip().split()
            if (userID == int(ln[0])):  # Se l'ID dell'Utente corrisponde a quello inserito, allora memorizza in ordine i voti corrispondenti
                lVoti.append(int(ln[2]))

    return lVoti

