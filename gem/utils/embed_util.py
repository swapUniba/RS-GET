import numpy as np
import copy as cp

def reorient(embed1, embed2):
    assert embed1.shape[1] == embed2.shape[1], ('Embedding dimension should be the same for both embeddings')
    n1, d = embed1.shape
    n2, d = embed2.shape
    if(n1 > n2):
        S = np.dot(embed2.T, embed1[0:n2,:])
    else:
        S = np.dot(embed2[0:n1,:].T, embed1)
    u, sig, v = np.linalg.svd(S)
    R = np.dot(u,v)
    reoriented_embed2 = np.dot(embed2, R)
    return reoriented_embed2, R



# Calcola la Similarita' di Embedding di 2 Item utilizzando la Similarita' del Coseno.
def embeddingsCosineSimilarity(embed1, embed2):

    assert embed1.__len__() == embed2.__len__(), ("La dimensione dei 2 Embedding deve essere la stessa")
    n = embed1.__len__()

    num = 0.0
    for k in range(0, n):
        num += (embed1[k]*embed2[k])

    denP1 = 0.0
    for k in range(0, n):
        denP1 += (embed1[k]*embed1[k])
    denP1 = np.sqrt(denP1)

    denP2 = 0.0
    for k in range(0, n):
        denP2 += (embed2[k]*embed2[k])
    denP2 = np.sqrt(denP2)

    den = denP1*denP2
    #print float(num)/float(den)
    return float(num) / float(den)



# Restituisce gli n Embedding piu' simili all'Embedding dell'Item dato in Input.
def embeddingsMoreLike(dataset, emb, itemEmbed, n):

    nEmb, dEmb = emb.shape  # nEmb: numero di Embedding degli Item; dEmb: dimensione degli Embedding
    embZero = np.zeros(dEmb)

    embCopyWithSim = np.zeros((nEmb, dEmb+2))       # Matrice Copia dell'Embedding del Grafo originale, essa conterra' una nuova colonna in cui
                                                    # si indichera' la similarita' con l'Embedding dell'Item dato in Input.
    # Compone la nuova Matrice Copia con una nuova colonna dove si indichera' la similarita' corrispondente
    for iEmb in range(0, nEmb):

        for iCol in range(0, dEmb):
            embCopyWithSim[iEmb, iCol] = emb[iEmb, iCol]

        if (list(emb[iEmb]) == list(embZero)) | (list(emb[iEmb]) == list(itemEmbed)):   # Se l'embedding e' nullo oppure corrisponde a quello dato in input
            embCopyWithSim[iEmb, dEmb] = -100.00
        else:
            embCopyWithSim[iEmb, dEmb] = embeddingsCosineSimilarity(itemEmbed, emb[iEmb])   # Scrive nella penultima colonna la similarita' corrispondente
            embCopyWithSim[iEmb, dEmb+1] = iEmb                 # Scrive nell'ultima colonna l'ID dell'Item corrispondente


    # Ordina le righe(embeddings) della Matrice Copia per similarita' decrescente
    switch = True
    while switch:
        switch = False
        for iEmb in range(0, nEmb-1):
            # Effettua lo scambio delle 2 righe considerate (Embeddings)
            if (embCopyWithSim[iEmb, dEmb]) < (embCopyWithSim[iEmb+1, dEmb]):
                arrApp = cp.copy(embCopyWithSim[iEmb])
                embCopyWithSim[iEmb] = cp.copy(embCopyWithSim[iEmb+1])
                embCopyWithSim[iEmb+1] = cp.copy(arrApp)
                switch = True


    lItems = []
    with open('gem/data/' + dataset + '/u1LIKE.base', 'r') as br:
        for line in br:
    	    ln = line.strip().split()
    	    lItems.append(int(ln[1]))
    l = list(set(lItems))  # Elimina i doppioni dalla lista
    l.sort()  # Ordina la lista che contiene tutti gli ID contenuti nel Grafo originale
    print "Numero di Item presenti nel file .base:", l.__len__()


    embsMoreLike = np.zeros((n, dEmb))  # Matrice che conterra' gli n Embedding piu' simili a quello dato in Input
    # Popola la Matrice che conterra' gli n Embedding piu' simili in ordine Decrescente
    iEmbML = 0
    iCopyWS = 0
    while iEmbML < n :
        isItem = False
        for iC in range(0, dEmb):
            if ((embCopyWithSim[iCopyWS, dEmb+1]) in lItems):
                embsMoreLike[iEmbML, iC] = cp.copy(embCopyWithSim[iCopyWS, iC])
                isItem = True
        if isItem:
            #print "\nID dell'Item: %d" % embCopyWithSim[iCopyWS, dEmb + 1]
            #print "Embedding dell'Item:\n", embsMoreLike[iEmbML]
            #print "Similarita' del coseno: %.16f" % embCopyWithSim[iCopyWS, dEmb]
            iEmbML = iEmbML + 1

        iCopyWS = iCopyWS + 1

    return embsMoreLike
