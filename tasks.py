import copy as cp
import numpy as np
from time import time
import os

from gem.utils import graph_util, evaluation_util, node_classification_util
from gem.evaluation import evaluate_node_classification as nc
from gem.evaluation import evaluate_link_prediction as lp
from gem.evaluation import visualize_embedding as ve
import matplotlib.pyplot as plt



# ESEGUE LA COSTRUZIONE DEGLI EMBEDDING
def buildEmbedding(dataset, G, methods):

    for embedding in methods:

        print 'Numero di Nodi: %d, Numero di Archi: %d' % (G.number_of_nodes(), G.number_of_edges())
        t1 = time()

        Y, t = embedding.learn_embedding(graph=G, edge_f=None, is_weighted=True, no_python=True)  # Costruisce l'embedding - Prende in input o un Grafo networkx o il file con la lista degli archi.
        print ("METODO: " + embedding._method_name + "\nDimensioni dell'Embedding: " + repr(embedding._d) + "\n\tTempo di costruzione: %f\n" % (time() - t1))
        #print Y

        if not os.path.exists("embs"):
            os.makedirs("embs")
        np.save('embs/embsLike_' + dataset + '_' + embedding._method_name + '_' + repr(embedding._d), Y, allow_pickle=True)
        del Y



# ESEGUE IL TASK DI LINK PREDICTION
def executeLinkPrediction(dataset, isDirected, method):

    G_train = graph_util.loadGraphFromEdgeListTxt('gem/datasets/' + dataset + '/u1LIKECompact.base', directed=isDirected)    # Carica il Grafo di Train
    G_test = graph_util.loadGraphFromEdgeListTxt('gem/datasets/' + dataset + '/u1LIKECompact.test', directed=isDirected)    # Carica il Grafo di Test
    G_total = graph_util.loadGraphFromEdgeListTxt('gem/datasets/' + dataset + '/u1LIKECompact.edgelist', directed=isDirected)    # Carica il Grafo totale (Train + Test)

    MAP = lp.evaluateStaticLinkPrediction(G_total, G_train, G_test, method, is_undirected=(not isDirected))

    print method.get_method_summary()
    print "MAP:", MAP



# ESEGUE IL TASK DI NODE CLASSIFICATION
def executeNodeClassification(dataset, embsLike):

    # Prende la lista degli Utenti presenti nel file .test
    usersList = node_classification_util.listUsers('gem/datasets/' + dataset + '/u1.test')
    #print "\nNumero di Utenti presenti nel file .test:", usersList.__len__()
    #print "\nLista degli Utenti presenti nel .test:\n", usersList

    microf1Sum = 0.0
    macrof1Sum = 0.0
    nUtentiTestati = 0

    for user in usersList:

        nUtentiTestati = nUtentiTestati + 1

        print "\n\n- ID UTENTE:", user

        # Creo una matrice contenente gli embedding degli Item graditi dall'Utente
        positiveExamples, positiveExamplesEmbs = node_classification_util.collectPositiveExamples(user, embsLike, 'gem/datasets/' + dataset + '/u1.base')
        #print "\nLista degli Item graditi dall'Utente (LIKE):\n", positiveExamples
        #print "\nEmbedding degli Item graditi dall'utente:\n", positiveExamplesEmbs

        # Creo una matrice contenente gli embedding degli Item NON graditi dall'Utente
        negativeExamples, negativeExamplesEmbs = node_classification_util.collectNegativeExamples(user, embsLike, 'gem/datasets/' + dataset + '/u1.base')
        #print "\nLista degli Item NON graditi dall'Utente (DISLIKE):\n", negativeExamples
        #print "\nEmbedding degli Item NON graditi dall'utente:\n", negativeExamplesEmbs

        # Creo una matrice contenente gli embedding degli Item da testare
        testItems, testItemsEmbs = node_classification_util.collectItemsTest(user, embsLike, 'gem/datasets/' + dataset + '/u1.test')
        #print "\nLista degli Item da testare dall'Utente:\n", testItems
        #print "\nEmbedding degli Item da testare dell'utente:\n", testItemsEmbs

        # Creo la lista dei Voti corretti degli Item da testare
        votiListCorrect = node_classification_util.listRatings(user, 'gem/datasets/' + dataset + '/u1.test')
        #print "\nLista dei voti corretti:\n", votiListCorrect


        try:
            X_train = np.concatenate((positiveExamplesEmbs, negativeExamplesEmbs))
        except:
            try:
                if positiveExamplesEmbs.shape[0] == 0:
                    X_train = cp.copy(negativeExamplesEmbs)
                if negativeExamplesEmbs.shape[0] == 0:
                    X_train = cp.copy(positiveExamplesEmbs)
            except:
                X_train = np.array([[]])
        #print "\nEmbedding di Training (X_train):\n", X_train

        y_train = []
        for i in range(0, positiveExamplesEmbs.shape[0]):
            y_train.append(1)
        for j in range( (positiveExamplesEmbs.shape[0]), (positiveExamplesEmbs.shape[0] + negativeExamplesEmbs.shape[0]) ):
            y_train.append(0)
        #print "\nEtichette di Training corrispondenti (y_train):\n", y_train

        X_test = cp.copy(testItemsEmbs)
        #print "\nX_test:\n", X_test

        y_test = cp.copy(votiListCorrect)
        #print "\nLista delle etichette corrette (y_test):\n", y_test


        micro, macro, pred = nc.evaluateNodeClassification(X_train, X_test, y_train, y_test)
        #print "\nmicro-f1:", micro
        #print "macro-f1:", macro

        microf1Sum = microf1Sum + micro
        macrof1Sum = macrof1Sum + macro


    print "\n\nMedia delle micro-f1:", microf1Sum / nUtentiTestati
    print "Media delle macro-f1:", macrof1Sum / nUtentiTestati
