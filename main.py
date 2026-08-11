import json
class libro():
    def __init__(self, titolo, autore, prezzo, disponibilità=True):
        self.titolo = titolo
        self.autore = autore
        self.prezzo = prezzo
        self.disponibilità = disponibilità

    def to_dict(self):
        return {
            "titolo": self.titolo,
            "autore": self.autore,
            "prezzo": self.prezzo,
            "disponibilità": self.disponibilità
        }        

    def dettagli(self):
        return f"Titolo: {self.titolo} | Autore: {self.autore} | Prezzo: €{self.prezzo:.2f} | Disponibile: {'SÌ' if self.disponibilità else 'NO'}"

        
class libreria():
    def __init__(self, nome_file="libreria.json"):
        self.nome_file = nome_file
        self.catalogo = {}

    def carica_dati(self):
        try:
            with open(self.nome_file, "r") as file:
                self.catalogo = json.load(file)
                print("DATI CARICATI\n")
        except FileNotFoundError:
            self.catalogo = {}
            print("Catalogo inizializzato da nuovo!")      

    def salva_dati(self):
        try:
            with open(self.nome_file, "w") as file:
                json.dump(self.catalogo, file, indent=4)
        except FileNotFoundError:
            print("Impossibile salvare: File non trovato")

    def aggiungi_libro(self, book):
        if book.titolo in self.catalogo:
            print("Errore: libro già presente!")
        else:
            self.catalogo[book.titolo] = book.to_dict()
            self.salva_dati()
            print("Libro aggiunto correttamente!\n")

    def cerca_libro(self, titolo):
        if titolo in self.catalogo:
            v = self.catalogo[titolo]
            print("\nDati libro:")
            print(f"Titolo: {v['titolo']} | Autore: {v['autore']} | Prezzo: €{v['prezzo']:.2f} | Disponibile: {'SÌ' if v['disponibilità'] else 'NO'}\n")
        else:
            print("Errore: Libro non trovato nel catalogo")

    def cambia_disponibilita(self, titolo, stato_bool):
        if titolo in self.catalogo:
            self.catalogo[titolo]["disponibilità"] = stato_bool
            self.salva_dati()
            print("Stato libro aggiornato correttamente!")
        else:
            print("Errore: Libro non trovato nel catalogo")

    def mostra_catalogo(self):
        print("\nElenco libri:")
        for c, v in self.catalogo.items():
            disp = "SÌ" if v.get("disponibilità", True) else "NO"
            print(f"- Titolo: {c} | Autore: {v['autore']} | Prezzo: €{v['prezzo']:.2f} | Disponibile: {disp}")

    def elimina_libro(self, titolo):
        if titolo in self.catalogo:
            del self.catalogo[titolo]
            self.salva_dati()
            print("Libro eliminato e catalogo aggiornato!")
        else:
            print("Errore: Titolo non trovato!")


#--- MENU PRINCIPALE ---
mia_libreria = libreria()
mia_libreria.carica_dati()

print("Scegli azione\n")
while True:
    try:
        s = int(input("""\n0) Esci dal programma
1) Aggiungi Libro
2) Cerca libro
3) Mostra Catalogo
4) Cambiare disponibilità
5) Eliminare un libro
-> """))
        if s not in [0, 1, 2, 3, 4, 5]:
            print("Errore: devi scegliere un numero tra 0 e 5")
            continue

        if s == 0:
            mia_libreria.salva_dati()
            print("Arrivederci!")
            exit()

        elif s == 1:
            titolo = input("Inserisci il titolo del libro: ").strip()
            if titolo in mia_libreria.catalogo:
                print("Errore: Libro già presente!")
                continue
            
            autore = input("Inserisci l'autore del libro: ").strip()
            
            while True:
                try:
                    prezzo = float(input("Inserisci il prezzo del libro(€): "))
                    if prezzo < 0:
                        print("Errore: il prezzo deve essere pari o maggiore di 0")
                        continue
                    break
                except ValueError:
                    print("Errore: Devi inserire un numero valido per il prezzo")

            while True:
                disponibilità = input("Il libro è disponibile? (si/no): ").lower().strip()[:2]
                if disponibilità not in ["s", "n", "si", "no"]:
                    print("Errore: rispondi con 'si' o 'no'")
                    continue
                disp_bool = True if disponibilità in ["s", "si"] else False
                break

            nuovo_libro = libro(titolo, autore, prezzo, disp_bool)
            mia_libreria.aggiungi_libro(nuovo_libro)

        elif s == 2:
            titolo = input("Inserisci il titolo del libro che cerchi: ").strip()
            mia_libreria.cerca_libro(titolo)

        elif s == 3:
            if mia_libreria.catalogo:
                mia_libreria.mostra_catalogo()  
            else:
                print("Catalogo Vuoto!")            

        elif s == 4:
            if mia_libreria.catalogo:
                mia_libreria.mostra_catalogo()  
                titolo = input("\nInserisci il titolo del libro da modificare: ").strip() 
                
                if titolo not in mia_libreria.catalogo:
                    print("Errore: Libro non trovato nel catalogo")
                    continue

                while True:
                    ans = input("Rendere il libro disponibile? (si/no): ").lower().strip()[:2]
                    if ans not in ["s", "n", "si", "no"]:
                        print("Errore: rispondi con 'si' o 'no'")
                        continue
                    nuovo_stato = True if ans in ["s", "si"] else False
                    break

                mia_libreria.cambia_disponibilita(titolo, nuovo_stato)
            else:
                print("Catalogo Vuoto!")             

        elif s == 5:
            if mia_libreria.catalogo:
                mia_libreria.mostra_catalogo()  
                titolo = input("\nInserisci il titolo del libro da eliminare: ").strip()
                mia_libreria.elimina_libro(titolo)
            else:
                print("Catalogo Vuoto!")

    except ValueError:
        print("Errore: Devi scegliere un numero")
