try: import cPickle as pickle
except: import pickle
import numpy as np
import networkx as nx
import random
import itertools
import time
import pdb
import copy as cp



def transform_DiGraph_to_adj(di_graph):
    n = di_graph.number_of_nodes()
    adj = np.zeros((n ,n))
    for st, ed, w in di_graph.edges(data='weight', default=1):
        adj[st, ed] = w
    return adj



def transform_adj_to_DiGraph(adj):
    n = adj.shape[0]
    di_graph = nx.DiGraph()
    di_graph.add_nodes_from(range(n))
    for i in xrange(n):
        for j in xrange(n):
            if(i != j):
                if(adj[i, j] > 0):
                    di_graph.add_edge(i, j, weight=adj[i, j])
    return di_graph



def sample_graph(di_graph, n_sampled_nodes=None):
    node_num = di_graph.number_of_nodes()
    if n_sampled_nodes and node_num > n_sampled_nodes:
        node_l = np.random.choice(node_num, n_sampled_nodes, replace=False)
        node_l_inv = {v: k for k, v in enumerate(node_l)}
        sampled_graph = nx.DiGraph()
        sampled_graph.add_nodes_from(range(n_sampled_nodes))
        for st, ed, w in di_graph.edges(data='weight', default=1):
            try:
                v_i = node_l_inv[st]
                v_j = node_l_inv[ed]
                sampled_graph.add_edge(v_i, v_j, weight=w)
            except:
                continue
        return sampled_graph, node_l
    else:
        return di_graph, np.arange(di_graph.number_of_nodes())



def randwalk_DiGraph_to_adj(di_graph, node_frac=0.1, n_walks_per_node=5, len_rw=2):
    t0 = time.time()
    n = di_graph.number_of_nodes()
    adj = np.zeros((n ,n))
    rw_node_num = int(node_frac * n)
    rw_node_list = np.random.choice(n, size=[rw_node_num], replace=False, p=None)
    for node in rw_node_list:
        for walk in range(n_walks_per_node):
            cur_node = node
            for step in range(len_rw):
                cur_neighbors = di_graph.neighbors(cur_node)
                try:
                    neighbor_node = np.random.choice(cur_neighbors)
                except:
                    continue
                try:
                    adj[cur_node, neighbor_node] = di_graph.get_edge_data(cur_node, neighbor_node)['weight']
                    adj[neighbor_node, cur_node] = di_graph.get_edge_data(cur_node, neighbor_node)['weight']
                except KeyError:
                    adj[cur_node, neighbor_node] = 1
                    adj[neighbor_node, cur_node] = 1
                cur_node = neighbor_node
    print('Time taken for random walk on graph with {0} nodes = {1}'.format(n, time.time() - t0))
    return adj



def addChaos(di_graphs, k):
    anomaly_time_steps = sorted(random.sample(range(len(di_graphs)), k))
    for t in anomaly_time_steps:
        n = di_graphs[t].number_of_nodes()
        e = di_graphs[t].number_of_edges()
        di_graphs[t] = nx.fast_gnp_random_graph(n, e/float(n*(n-1)), seed=None, directed=False)
        di_graphs[t] = di_graphs[t].to_directed()
    return di_graphs, anomaly_time_steps



def addNodeAnomalies(di_graphs, p, k):
    anomaly_time_steps = sorted(random.sample(range(len(di_graphs)), k))
    for t in anomaly_time_steps:
        n_nodes= di_graphs[t].number_of_nodes()
        anomalous_nodes_idx = np.random.choice([0,1], size=(n_nodes, 1), p=(1-p, p))
        node_list = np.array(di_graphs[t].nodes())
        node_list = node_list.reshape((n_nodes, 1))
        anomalous_nodes = np.multiply(anomalous_nodes_idx, node_list)
        anomalous_nodes = anomalous_nodes[anomalous_nodes > 0]
        # pdb.set_trace()
        di_graphs[t].add_edges_from(itertools.product(list(anomalous_nodes), range(n_nodes)))
        di_graphs[t].add_edges_from(itertools.product(range(n_nodes), list(anomalous_nodes)))
        print('Nodes: %d, Edges: %d' % (di_graphs[t].number_of_nodes(), di_graphs[t].number_of_edges()))
    return anomaly_time_steps



def saveGraphToEdgeListTxt(graph, file_name):
    with open(file_name, 'w') as f:
        f.write('%d\n' % graph.number_of_nodes())
        f.write('%d\n' % graph.number_of_edges())
        for i, j, w in graph.edges(data='weight', default=1):
            f.write('%d %d %f\n' % (i, j, w))



def saveGraphToEdgeListTxtn2v(graph, file_name):
    with open(file_name, 'w') as f:
        for i, j, w in graph.edges(data='weight', default=1):
            f.write('%d %d %f\n' % (i, j, w))



def loadGraphFromEdgeListTxt(file_name, directed=True):
    with open(file_name, 'r') as f:
        #n_nodes = f.readline()
        #f.readline() # Discard the number of edges
        if directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()
        for line in f:
            edge = line.strip().split()
            if len(edge) == 3:   # Se il file contiene i pesi degli archi
                w = float(edge[2])      # Assegna alla variabile 'w' il peso dell'arco presente nel file
            else:
                w = 1.0     # Se non si e' inserito un peso, assegna peso 1.0
            G.add_edge(int(edge[0]), int(edge[1]), weight=w)
    return G



# Carica l'embedding temporaneo generato da node2vec (funzione modificata al fine di utilizzare dataset composti da ID non compattati).
def loadEmbedding(file_name):
    lNodes = []

    with open(file_name, 'r') as br:
        for line in br:
    	    ln = line.strip().split()
            if (ln.__len__() != 2 ):
    	        lNodes.append(int(ln[0]))
    lNodes = list(set(lNodes))  # Elimina i doppioni dalla lista
    lNodes.sort()
    nMax = (lNodes[(lNodes.__len__() - 1)]) + 1

    with open(file_name, 'r') as f:
        n, d = f.readline().strip().split()     # n: numero di righe (relazioni)    # d: dimensione dell'embedding
        X = np.zeros((int(nMax), int(d)))
        for line in f:  # scorre le linee del file in lettura
            emb = line.strip().split()  # strip() elimina tutti gli spazi prima dell'inizio della stringa e dopo la fine della stringa,  # split() crea un vettore composto dalle singole stringhe della linea
            emb_fl = [float(emb_i) for emb_i in emb[1:]]    # Prende il secondo e terzo elemento di ogni riga della matrice
            X[int(emb[0]), :] = emb_fl
        #print X
    return X



def loadSBMGraph(file_prefix):
    graph_file = file_prefix + '_graph.gpickle'
    G = nx.read_gpickle(graph_file)
    node_file = file_prefix + '_node.pkl'
    with open(node_file, 'rb') as fp:
        node_community = pickle.load(fp)
    return (G, node_community)



def loadRealGraphSeries(file_prefix, startId, endId):
    graphs = []
    for file_id in range(startId, endId + 1):
        graph_file = file_prefix + str(file_id) + '_graph.gpickle'
        graphs.append(nx.read_gpickle(graph_file))
    return graphs



def saveRealGraphSeries(G, file_prefix='graphs/day_'):
    for idx in range(len(G)):
        f_name = file_prefix + str(idx) + "_graph.gpickle"
        # cPickle.dump(G[idx], open(f_name, 'wb'))
        nx.write_gpickle(G[idx], f_name)



def loadDynamicSBmGraph(file_perfix, length):
    graph_files = ['%s_%d_graph.gpickle' % (file_perfix, i) for i in xrange(length)]
    info_files = ['%s_%d_node.pkl' % (file_perfix, i) for i in xrange(length)]

    graphs = [nx.read_gpickle(graph_file) for graph_file in graph_files]
    
    nodes_comunities = []
    perturbations = []
    for info_file in info_files:
        with open(info_file, 'rb') as fp:
            node_infos = pickle.load(fp)
            nodes_comunities.append(node_infos['community'])
            perturbations.append(node_infos['perturbation'])

    return zip(graphs, nodes_comunities, perturbations)



def saveDynamicSBmGraph(file_perfix, dynamic_graphs):
    length = len(dynamic_graphs)
    graph_files = ['%s_%d_graph.gpickle' % (file_perfix, i) for i in xrange(length)]
    info_files = ['%s_%d_node.pkl' % (file_perfix, i) for i in xrange(length)]

    for i in xrange(length):
        # save graph
        nx.write_gpickle(dynamic_graphs[i][0], graph_files[i])
        # save additional node info
        with open(info_files[i], 'wb') as fp:
            node_infos = {}
            node_infos['community'] = dynamic_graphs[i][1]
            node_infos['perturbation'] = dynamic_graphs[i][2]
            pickle.dump(node_infos, fp)

