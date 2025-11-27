from database.DB_connect import DBConnect

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def get_all_hub():
        # Prendo tutti gli hub della tabella hub
        connessione = DBConnect.get_connection()
        cursor = connessione.cursor()
        query = "SELECT * FROM hub"
        cursor.execute(query)
        risultato = cursor.fetchall()
        cursor.close()
        connessione.close()
        return risultato

    @staticmethod
    def get_tratte_aggregate():
        # Uso la query più complicata per restituire le tratte A-B non orientate
        connessione = DBConnect.get_connection()
        cursor = connessione.cursor()
        # I metodi LEAST e GREATEST permettono di evitare i duplicati perchè che la tratta sia
        # A -> B o B-> A diventano comunque (A, B); poi seleziono il nome di entrambi gli hub e
        # i rispettivi stati perchè li voglio nella stampa finale del controller; poi seleziono la
        # somma dei valori_merce e conto quante spedizioni ci sono nella tratta;
        query = '''SELECT LEAST(id_hub_origine, id_hub_destinazione) AS hub1, 
                            GREATEST(id_hub_origine, id_hub_destinazione) AS hub2,
                            h1.nome AS nome_hub1,
                            h1.stato AS stato_hub1,
                            h2.nome AS nome_hub2,
                            h2.stato AS stato_hub2,
                            SUM(valore_merce) AS totale_valore,
                            COUNT(*) AS num_spedizioni
                   FROM spedizione s
                   JOIN hub h1 ON h1.id = LEAST(id_hub_origine, id_hub_destinazione)
                   JOIN hub h2 ON h2.id = GREATEST(id_hub_origine, id_hub_destinazione)
                   GROUP BY hub1, hub2'''
        cursor.execute(query)
        risultato = cursor.fetchall()
        cursor.close()
        connessione.close()
        return risultato

