from sklearn import model_selection as sk_ms
from sklearn.multiclass import OneVsRestClassifier as oneVr
from sklearn.linear_model import LogisticRegression as lr
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score

import numpy as np
from sklearn.multiclass import OneVsOneClassifier as oneVone


class TopKRanker(oneVr):

    # Metodo proveniente della Libreria GEM, modificato per poter valutare il Task di Node Classification sui Dataset a disposizione
    def predict(self, X, top_k_list):

        assert X.shape[0] == len(top_k_list)    # Il numero di righe della Matrice X_test deve essere lo stesso del numero dei top_k della lista delle etichette da testare

        probs = np.asarray(super(TopKRanker, self).predict_proba(X))    # Converte l'output della funzione( 'predict_proba()' che restituisce una stima delle propabilita' delle etichette) in una Matrice
        prediction = np.zeros((X.shape[0], 1))
        #print "\nprobs:\n", probs

        # Compone il vettore delle etichette predette considerando l'etichetta avente maggiore probabilita'
        for i in range(0, probs.shape[0]):
            if (probs[i, 0] > probs[i, 1]):
                prediction[i] = 0
            else:
                prediction[i] = 1

        return prediction



# Metodo proveniente dalla Libreria GEM, modificato per poter valutare il Task di Node Classification sui Dataset a disposizione
def evaluateNodeClassification(X_train, X_test, Y_train, Y_test):

    classif2 = TopKRanker(lr())
    classif2.fit(X_train, Y_train)

    prediction = classif2.predict(X_test, Y_test)
    #print "\nEtichette predette:\n", prediction

    micro = f1_score(Y_test, prediction, average='micro')   # Metodo della libreria sklearn per il calcolo della micro f1
    macro = f1_score(Y_test, prediction, average='macro')   # Metodo della libreria sklearn per il calcolo della macro f1

    return (micro, macro, prediction)
