from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """

        # Ripulisco il grafo se era già costruito
        self.G.clear()
        # Definisco la lista di tutti gli hub
        hubs = DAO.get_all_hub()
        # Aggiungo l'hub come nodo del grafo
        for hub in hubs:
            hub_id = hub[0]
            self.G.add_node(hub_id)
        # Definisco la lista di tutte le tratte
        tratte = DAO.get_tratte_aggregate()
        # Calcolo il guadagno medio sulla tratta
        for hub1, hub2, nome_hub1, stato_hub1, nome_hub2, stato_hub2, totale_valore, num_spedizioni in tratte:
            media = totale_valore / num_spedizioni
            # Se il valore del guadagno medio è >= della soglia allora aggiungo la tratta
            if media >= threshold:
                self.G.add_edge(hub1, hub2,
                                weight=media,
                                nome1=nome_hub1,
                                stato1 = stato_hub1,
                                nome2=nome_hub2,
                                stato2=stato_hub2,
                                )

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """

        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """

        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """

        risultato = []
        for u, v, data in self.G.edges(data=True):
            nome1 = data['nome1']
            stato1 = data['stato1']
            nome2 = data['nome2']
            stato2 = data['stato2']
            weight = data['weight']
            risultato.append((nome1, stato1, nome2, stato2, weight))
        return risultato

