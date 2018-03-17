from gem.evaluation import metrics
from gem.utils import evaluation_util, graph_util
import networkx as nx



# Metodo della Libreria GEM, modificato per poter valutare il Task di Link Prediction sui Dataset a disposizione (l'unica differenza e' che NON effettua la divisione random per creare train e test)
def evaluateStaticLinkPrediction(digraph, train_digraph, test_digraph, graph_embedding, is_undirected=True, n_sample_nodes=None, sample_ratio_e=None, no_python=False):

    node_num = digraph.number_of_nodes()

    nodesTotalGraph = digraph.nodes()
    nodesTrainGraph = train_digraph.nodes()
    nodesTestGraph = test_digraph.nodes()

    for node in nodesTotalGraph:
        if not (node in nodesTrainGraph):
            train_digraph.add_node(int(node))
        if not (node in nodesTestGraph):
            test_digraph.add_node(int(node))


    if not nx.is_connected(train_digraph.to_undirected()):      # Se il Grafo di Training non e' connesso

        train_digraph = max(nx.weakly_connected_component_subgraphs(train_digraph),key=len)
        tdl_nodes = train_digraph.nodes()   # Contiene i nodi del Grafo di Training connesso
        nodeListMap = dict(zip(tdl_nodes, range(len(tdl_nodes))))
        nx.relabel_nodes(train_digraph, nodeListMap, copy=False)    # Rietichetta i nodi modificando l'ID originale in 'numero di nodo'

        test_digraph = test_digraph.subgraph(tdl_nodes)     # Il nuovo Grafo di Test sara' composto soltanto dai nodi che sono anche presenti in tdl_nodes
        nx.relabel_nodes(test_digraph, nodeListMap, copy=False)


    X, _ = graph_embedding.learn_embedding(graph=train_digraph, no_python=no_python)    # Costruisce l'Embedding del Grafo

    node_l = None
    if n_sample_nodes:
        test_digraph, node_l = graph_util.sample_graph(test_digraph, n_sample_nodes)
        X = X[node_l]


    # VALUTAZIONE

    if sample_ratio_e:
        eval_edge_pairs = evaluation_util.getRandomEdgePairs(node_num, sample_ratio_e, is_undirected)
    else:
        eval_edge_pairs = None

    estimated_adj = graph_embedding.get_reconstructed_adj(X, node_l)
    predicted_edge_list = evaluation_util.getEdgeListFromAdjMtx(estimated_adj, is_undirected=is_undirected, edge_pairs=eval_edge_pairs)
    filtered_edge_list = [e for e in predicted_edge_list if not train_digraph.has_edge(e[0], e[1])]

    MAP = metrics.computeMAP(filtered_edge_list, test_digraph) # Calcola la Mean Average Precision
    #prec_curv, _ = metrics.computePrecisionCurve(filtered_edge_list, test_digraph)

    #return (MAP, prec_curv)
    return MAP
