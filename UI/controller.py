import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """

        # Controllo che il valore inserito come soglia non sia None, non sia solo spazi e non sia
        # un valore non numerico
        valore = self._view.guadagno_medio_minimo.value
        if valore is None or valore.strip()=="":
            self._view.show_alert("Inserire un valore numerico!")
            return
        try:
            soglia = float(valore)
        except ValueError:
            self._view.show_alert("Inserire un valore numerico!")
            return
        self._model.costruisci_grafo(soglia)
        num_nodi = self._model.get_num_nodes()
        num_archi = self._model.get_num_edges()
        tratte = self._model.get_all_edges()
        # Ripulisco la lista di visualizzazione
        self._view.lista_visualizzazione.controls.clear()
        # Aggiungo il numero di hub, ovvero il numero di nodi
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di hub : {num_nodi}")
        )
        # Aggiungo il numero di tratte valide, ovvero il numero di archi
        self._view.lista_visualizzazione.controls.append(
            ft.Text(f"Numero di Tratte Valide : {num_archi}")
        )
        self._view.lista_visualizzazione.controls.append(ft.Divider())
        # Faccio la stampa finale e uso enumerate(tratte, start = 1) perchè così davanti ad ogni riga
        # mette un numero progressivo che parte da 1 fino al numero di tratte
        for i, (nome1, stato1, nome2, stato2, weight) in enumerate(tratte, start=1):
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"{i}) {nome1} ({stato1}) -> {nome2} ({stato2}) -- Guadagno medio per spedizione : {weight:.2f} €")
            )
        self._view.update()


