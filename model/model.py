import networkx as nx
from unicodedata import decimal

from database.dao import DAO


class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        # TODO
        self.G = nx.Graph()

        self.id_map = {} # id rifugio
        self.rifugi = [] # lista rifugi
        self.pesi = []
        self.connessioni =  [] #connessioni filtrate per anno

    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        # TODO
        peso = 0
        self.rifugi = DAO.readAllRifugi()
        self.id_map = {r.id: r for r in self.rifugi}

        self.connessioni = DAO.readAllConnessioni(year)
        edges = []
        for c in self.connessioni:
            if c.id_rifugio1 in self.id_map and c.id_rifugio2 in self.id_map:
                r1 = self.id_map[c.id_rifugio1]
                r2 = self.id_map[c.id_rifugio2]
                if c.difficolta == "facile":
                    peso = float(c.distanza)*1
                elif c.difficolta == "media":
                    peso = float(c.distanza)*1.5
                elif c.difficolta == "difficile":
                    peso = float(c.distanza)*2
                self.pesi.append(peso)
                edges.append((r1.id, r2.id, peso))
        self.G.add_weighted_edges_from(edges)
        print (self.G)
        #print (edges)



    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        # TODO
        return min(self.pesi), max(self.pesi)


    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        # TODO
        min = 0
        for (u,v,peso) in self.G.edges.data("weight"):
            if peso < soglia:
                min +=1
        max = 0
        for (u,v,peso) in self.G.edges.data("weight"):
            if peso > soglia:
                max +=1
        return min,max

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
    def cammino_minimo(self, soglia):
        grafo = nx.Graph()

        for (u,v,peso) in self.G.edges.data("weight"):
            if peso > soglia:
                grafo.add_edge(u, v, weight=peso)

        best_path = []
        best_weight = float("inf")

        nodi = list(grafo.nodes())

        for i in range (len(nodi)):
            for j in range (i+1, len(nodi)):
                s = nodi[i]
                t = nodi[j]

                try:
                    path = nx.shortest_path(grafo, s, t, weight= "weight")
                    if len(path) < 3:
                        continue

                    peso_tot = nx.path_weight(grafo, path, weight="weight")

                    if peso_tot < best_weight:
                        best_weight = peso_tot
                        best_path = path
                except nx.NetworkXNoPath:
                    continue

        return best_path

    def cammino_minimo_ricorsivo(self,soglia):
        self.best_path = []
        self.best_weight = float("inf")

        nodi = list(self.G.nodes())

        for i in range (len(nodi)):
            for j in range (i+1, len(nodi)):
                start = nodi[i]
                end = nodi[j]
                self._dfs(start, end, soglia,[start],0)

        return self.best_path

    def _dfs(self,nodo_corrente, target, soglia, path_corrente, peso_corrente):
        if nodo_corrente == target:
            if len(path_corrente) >=3:
                if peso_corrente < self.best_weight:
                    self.best_weight = peso_corrente
                    self.best_path = path_corrente.copy()
            return

        for vicino in self.G.neighbors(nodo_corrente):
            if vicino in path_corrente:
                continue

            peso_arco = self.G[nodo_corrente][vicino]["weight"]

            if peso_arco <= soglia:
                continue

            path_corrente.append(vicino)
            self._dfs(vicino,target,soglia,path_corrente,peso_corrente+peso_arco)
            path_corrente.pop()


