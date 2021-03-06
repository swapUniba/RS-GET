disp_avlbl = True
import os
if 'DISPLAY' not in os.environ:
    disp_avlbl = False
    import matplotlib
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy.io as sio
import scipy.sparse as sp
import scipy.sparse.linalg as lg
from time import time
import copy as cp

import sys
sys.path.append('./')
sys.path.append(os.path.realpath(__file__))

from .static_graph_embedding import StaticGraphEmbedding
from gem.utils import graph_util, plot_util
from gem.evaluation import visualize_embedding as viz



class HOPE(StaticGraphEmbedding):



	def __init__(self, nomeDataset, d, beta):
		self._d = d
		self._method_name = 'HOPE'#_beta_%f' % beta
		self._X = None
		self._beta = beta
		self._nomeDataset = nomeDataset



	def get_method_name(self):
		return self._method_name



	def get_method_summary(self):
		return '%s_%d' % (self._method_name, self._d)



	def learn_embedding(self, graph=None, edge_f=None, is_weighted=False, no_python=False):
		if not graph and not edge_f:
			raise Exception('graph/edge_f needed')
		if not graph:
			graph = graph_util.loadGraphFromEdgeListTxt(edge_f)

		t1 = time()
		# A = nx.to_scipy_sparse_matrix(graph)
		# I = sp.eye(graph.number_of_nodes()) 
		# M_g = I - self._beta*A
		# M_l = self._beta*A
		A = nx.to_numpy_matrix(graph)	# Crea la matrice di adiacenza del Grafo 'graph'

		#print "Graph:\n", graph
		#print "Matrice di adiacenza del Grafo:\n", A

		M_g = np.eye(graph.number_of_nodes()) - self._beta*A
		M_l = self._beta*A
		S = np.dot(np.linalg.inv(M_g), M_l)

		u, s, vt = lg.svds(S, k=self._d//2) 
		X1 = np.dot(u, np.diag(np.sqrt(s)))
		X2 = np.dot(vt.T, np.diag(np.sqrt(s)))
		t2 = time()
		self._X = np.concatenate((X1, X2), axis=1)

		p_d_p_t = np.dot(u, np.dot(np.diag(s), vt))
		eig_err = np.linalg.norm(p_d_p_t - S)
		print('SVD error (low rank): %f' % eig_err)

		# p_d_p_t = np.dot(self._X, np.dot(w[1:self._d+1, 1:self._d+1], self._X.T))
		# eig_err = np.linalg.norm(p_d_p_t - L_sym)
		# print 'Laplacian reconstruction error (low rank approx): %f' % eig_err


		# BLOCCO DI ISTRUZIONI DA ESEGUIRE SE GLI ID DEL DATASET NON SONO COMPATTI
		listNodes = graph.nodes()
		listNodes = list(set(listNodes))  # Elimina i doppioni dalla lista
		listNodes.sort()  # Ordina la lista che contiene tutti gli ID contenuti nel Grafo originale
		nA = np.asarray(listNodes, dtype=int)
		dE = self._d
		nR = (nA.max()) + 1
		XX = np.zeros((nR, dE))
		for i in range(0, nA.__len__()):
			XX[nA[i]] = cp.copy(self._X[i])
		self._X = np.zeros((nR, dE))
		self._X = cp.copy(XX)


		return self._X, (t2-t1)



	def get_embedding(self):
		return self._X



	def get_edge_weight(self, i, j):
		return np.dot(self._X[i, :self._d//2], self._X[j, self._d//2:])



	def get_reconstructed_adj(self, X=None, node_l=None):
		if X is not None:
			node_num = X.shape[0]
			self._X = X
		else:
			node_num = self._node_num
		adj_mtx_r = np.zeros((node_num, node_num)) # G_r is the reconstructed graph
		for v_i in range(node_num):
			for v_j in range(node_num):
				if v_i == v_j:
					continue
				adj_mtx_r[v_i, v_j] = self.get_edge_weight(v_i, v_j)
		return adj_mtx_r



if __name__ == '__main__':

	edge_f = 'data/lastfm/u1.edgelist'# load graph
	G = graph_util.loadGraphFromEdgeListTxt(edge_f, directed=False)
	G = G.to_directed()
	res_pre = 'results/testKarate'

	print('Num nodes: %d, num edges: %d' % (G.number_of_nodes(), G.number_of_edges()))
	t1 = time()
	embedding = HOPE(4, 0.01)
	embedding.learn_embedding(graph=G, edge_f=None, is_weighted=True, no_python=True)
	print('HOPE:\n\tTraining time: %f' % (time() - t1))

	viz.plot_embedding2D(embedding.get_embedding()[:, :2], di_graph=G, node_colors=None)
	plt.show()

