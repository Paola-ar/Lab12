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
                edges.append((r1, r2,peso))
        self.G.add_weighted_edges_from(edges)
        print (self.G)



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
        for (u,v,w) in self.G.edges.data():
            if w < soglia:
                min +=1
        max = 0
        for (u,v,w) in self.G.edges.data():
            if w > soglia:
                max +=1
        return min,max

    """Implementare la parte di ricerca del cammino minimo"""
    # TODO
