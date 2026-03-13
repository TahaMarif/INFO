class Biblio: 
    def __init__(self,nom,prenom,adresse,id, lecteur = []):
        self.__lecteur = lecteur
        Lecteur.__init__(self,nom,prenom,adresse,id)

    def add_lecteur(self,nom):
        self.__lecteur.append(nom)


class Lecteur:
    def __init__(self,nom,prenom,adresse,numero,emprunt = 0):
        self.__nom = nom 
        self.__prenom = prenom
        self.__adresse = adresse
        self.__numero = numero 
        self.__emprunt = emprunt
    
    def __str__(self):
        return f"[{self.__numero}] {self.__prenom} {self.__nom} - {self.__adresse}"
    def get_nom(self):
        return self.__nom
    def get_prenom(self):
        return self.__prenom
    def get_adresse(self):
        return self.__adresse
    def get_numero(self):
        return self.__id
    def get_nb_emprunts(self):
        return self.__emprunt
    def set_nom(self,nom):
        self.__nom = nom 
    def set_prenom(self,prenom): 
        self.__prenom = prenom 
    def set_adresse(self,adresse):
        self.__adresse = adresse 
    def set_numero(self,id):
        self.__id = id
    def set_nb_emprunts(self,emprunt):
        self.__emprunt = emprunt

        
class Livre:
    def __init__(self,titre,auteur,num,nombre):
        self.__titre = titre 
        self.__auteur = auteur 
        self.__num = num 
        self.__nombre = nombre 

    def get_titre(self):
        return self.__titre
    def get_auteur(self):
        return self.__auteur
    def get_nombre(self):
        return self.__nombre
    def get_num(self): 
        return self.__num
    def get_nb_total(self):
        return self.__nombre
    def set_nb_total(self,nb):
        self.__nombre = nb


class Bibliotheque:
    def __init__(self, nom):
        self.nom = nom
        self.lecteurs = []    # liste de Lecteur
        self.livres = []      # liste de Livre
        self.emprunts = []    # liste de Emprunt

    # ---------- LECTEURS ----------

    def ajouter_lecteur(self, numero, nom, prenom, adresse):
        # Vérifier que le numéro est unique
        if any(l.numero == numero for l in self.lecteurs):
            print(f"Erreur : le numéro lecteur {numero} existe déjà.")
            return
        self.lecteurs.append(Lecteur(numero, nom, prenom, adresse))
        print(f"Lecteur ajouté : {prenom} {nom}")

    def rechercher_lecteur_par_numero(self, numero):
        for l in self.lecteurs:
            if l.numero == numero:
                return l
        return None

    def rechercher_lecteur_par_nom(self, nom):
        return [l for l in self.lecteurs if l.nom.lower() == nom.lower()]

    def retirer_lecteur(self, numero):
        lecteur = self.rechercher_lecteur_par_numero(numero)
        if not lecteur:
            print("Lecteur introuvable.")
            return
        # Vérifier qu'il n'a pas d'emprunt en cours
        if any(e.lecteur == lecteur for e in self.emprunts):
            print(f"Impossible : {lecteur.prenom} {lecteur.nom} a des emprunts en cours.")
            return
        self.lecteurs.remove(lecteur)
        print(f"Lecteur {lecteur.prenom} {lecteur.nom} retiré.")

    # ---------- LIVRES ----------

    def ajouter_livre(self, numero, titre, auteur, nb_exemplaires):
        if any(l.numero == numero for l in self.livres):
            print(f"Erreur : le numéro livre {numero} existe déjà.")
            return
        self.livres.append(Livre(numero, titre, auteur, nb_exemplaires))
        print(f"Livre ajouté : '{titre}'")

    def rechercher_livre_par_numero(self, numero):
        for l in self.livres:
            if l.numero == numero:
                return l
        return None

    def rechercher_livre_par_titre(self, titre):
        return [l for l in self.livres if titre.lower() in l.titre.lower()]

    def retirer_exemplaire(self, numero_livre):
        livre = self.rechercher_livre_par_numero(numero_livre)
        if not livre:
            print("Livre introuvable.")
            return
        if livre.nb_disponibles == 0:
            print("Aucun exemplaire disponible à retirer (tous empruntés).")
            return
        livre.nb_exemplaires -= 1
        livre.nb_disponibles -= 1
        print(f"Exemplaire retiré. Reste {livre.nb_exemplaires} exemplaire(s).")
        # Supprimer le livre si plus aucun exemplaire
        if livre.nb_exemplaires == 0:
            self.livres.remove(livre)
            print(f"Le livre '{livre.titre}' n'a plus d'exemplaires, il est retiré du catalogue.")

    # ---------- EMPRUNTS ----------

    def emprunter(self, numero_lecteur, numero_livre):
        lecteur = self.rechercher_lecteur_par_numero(numero_lecteur)
        livre = self.rechercher_livre_par_numero(numero_livre)

        if not lecteur:
            print("Lecteur introuvable.")
            return
        if not livre:
            print("Livre introuvable.")
            return
        if livre.nb_disponibles == 0:
            print(f"Aucun exemplaire disponible pour '{livre.titre}'.")
            return
        # Vérifier que le lecteur n'a pas déjà ce livre
        if any(e.lecteur == lecteur and e.livre == livre for e in self.emprunts):
            print(f"{lecteur.prenom} {lecteur.nom} a déjà emprunté '{livre.titre}'.")
            return

        emprunt = Emprunt(lecteur, livre)
        self.emprunts.append(emprunt)
        livre.nb_disponibles -= 1
        print(f"Emprunt enregistré : '{livre.titre}' → {lecteur.prenom} {lecteur.nom}")

    def retourner(self, numero_lecteur, numero_livre):
        lecteur = self.rechercher_lecteur_par_numero(numero_lecteur)
        livre = self.rechercher_livre_par_numero(numero_livre)

        if not lecteur or not livre:
            print("Lecteur ou livre introuvable.")
            return

        emprunt = next(
            (e for e in self.emprunts if e.lecteur == lecteur and e.livre == livre),
            None
        )
        if not emprunt:
            print("Aucun emprunt correspondant trouvé.")
            return

        self.emprunts.remove(emprunt)
        livre.nb_disponibles += 1
        print(f"Retour enregistré : '{livre.titre}' rendu par {lecteur.prenom} {lecteur.nom}")

    # ---------- ÉTATS ----------

    def lister_lecteurs(self):
        print(f"\n=== Lecteurs de '{self.nom}' ({len(self.lecteurs)}) ===")
        for l in self.lecteurs:
            print(l)

    def lister_livres(self):
        print(f"\n=== Livres de '{self.nom}' ({len(self.livres)}) ===")
        for l in self.livres:
            print(l)

    def lister_emprunts(self):
        print(f"\n=== Emprunts de '{self.nom}' ({len(self.emprunts)}) ===")
        for e in self.emprunts:
            print(e)