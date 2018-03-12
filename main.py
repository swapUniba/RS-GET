import numpy as np
import networkx as nx
import tasks, uriHandler

from gem.utils import graph_util, evaluation_util, plot_util, embed_util, dataset_statistics, dataset_util

from gem.embedding.hope     import HOPE
from gem.embedding.lap      import LaplacianEigenmaps
from gem.embedding.lle      import LocallyLinearEmbedding
from gem.embedding.node2vec import node2vec
from gem.embedding.sdne     import SDNE



# SERIE DI METODI RELATIVI ALLE STATISTICHE DEI DATASET

dataset = "lastfm"
#print "Numero di Utenti del Dataset:", dataset_statistics.numberUsers(dataset)
#print "Numero di Item presenti nel Dataset:", dataset_statistics.numberItems(dataset)
#print "Numero di voti positivi nel .test:", dataset_statistics.numberPositiveRatings(dataset)
#print "Numero di voti negativi nel .test:", dataset_statistics.numberNegativeRatings(dataset)
#print "Numero di utenti in", dataset, "considerando sia Training che Test:", dataset_statistics.numberUsersBaseAndTest(dataset)
#print "Numero di items in", dataset, "considerando sia Training che Test:", dataset_statistics.numberItemsBaseAndTest(dataset)
#print "Numero di proprieta' in", dataset, ":", dataset_statistics.numberProperties(dataset)



# SERIE DI METODI UTILI

#dataset_util.createDisgiuntiBaseTest(dataset)
#dataset_util.constructIDCompactLikeDislike(dataset)
#dataset_util.createOneDatasetWithAllRatings(dataset)



# BLOCCO DI ISTRUZIONI DA ESEGUIRE LA PRIMA VOLTA CHE SI USA IL TASK 'LINK PREDICTION' SU UN NUOVO DATASET

#dataset_util.createLikeBase(dataset)      # Prende solo le relazioni positive del Training
#dataset_util.createLikeTest(dataset)      # Prende solo le relazioni positive del Test
#dataset_util.constructIDCompactLike(dataset)      # Costruisce gli ID compatti nel Train e Test (considerando entrambi, quindi ID uguali continueranno a corrispondere)
#dataset_util.createBaseTestInOne(dataset)     # Concatena i dataset Train e Test compattati prima per formare Edgelist (Dataset che conterra' sia gli archi del Grafo di Training che quelli del Grafo di Test)



# BLOCCO DI ISTRUZIONI UTILI AD ESEGUIRE IL MAPPING DEI DATASET

#uriHandler.obtainSubjectPredicateObject(dataset)   # Chiamo il metodo che si occupa dell'esecuzione della Query e della serializzazione dei risultati
#uriHandler.createIDfromObjectUri(dataset)  # Chiamo il metodo che si occupa della trasformazione degli oggetti ottenuti in ID univoci
#uriHandler.deleteNotUniquePairs(dataset)   # Chiamo il metodo che si occupa dell'eliminazione delle coppie ripetute piu' volte nel file contenente la lista degli archi (ID-Item -> ID-Oggetto)
#dataset_util.concatenateUtenteItem_ItemObject("librarything")
#dataset_util.constructIDCompactBaseTestItemObject("librarything")
#uriHandler.deleteRelations("librarything")



# ESEGUE LA COSTRUZIONE DEGLI EMBEDDING

dataset = "lastfm"
G = graph_util.loadGraphFromEdgeListTxt('gem/datasets/' + dataset + '/u1LIKE.base', directed=True)    # Carica il Grafo

dimensions = []
#dimensions.append(64)
#dimensions.append(128)
#dimensions.append(256)
#dimensions.append(512)
for dim in dimensions:

    methods = []
    #methods.append(HOPE(dataset, dim, 0.01))
    #methods.append(LaplacianEigenmaps(dataset, dim))
    #methods.append(LocallyLinearEmbedding(dataset, dim))
    #methods.append(node2vec(dataset, dim, 1, 80, 10, 10, 1, 1))
    #methods.append(SDNE(d=dim, beta=5, alpha=1e-5, nu1=1e-6, nu2=1e-6, K=3,n_units=[50, 15,], rho=0.3, n_iter=50, xeta=0.01,n_batch=500,
    #               modelfile=['intermediate/enc_model.json', 'intermediate/dec_model.json'],
    #               weightfile=['intermediate/enc_weights.hdf5', 'intermediate/dec_weights.hdf5']))

    tasks.buildEmbedding(dataset, G, methods)

#exit()



# CARICA L'EMBEDDING COSTRUITO ED ESEGUE IL TASK DI NODE CLASSIFICATION

dataset = "lastfm"
method = "LaplacianEigenmaps"
dim = 128

print "\nDataset:", dataset, "- Metodo:", method, "- Dimensioni degli Embedding:", repr(dim)
embsLike = np.load('embs/embsLike_' + dataset + '_' + method + '_' + repr(dim) + '.npy', allow_pickle=True)
tasks.executeNodeClassification(dataset, embsLike)

exit()



# ESEGUE IL TASK DI LINK PREDICTION

dataset = "lastfm"
method = node2vec(dataset, 128, 1, 80, 10, 10, 1, 1)   # METODO, DATASET E DIMENSIONI DA TESTARE PER IL TASK DI LINK PREDICTION
tasks.executeLinkPrediction(dataset, True, method)

exit()
