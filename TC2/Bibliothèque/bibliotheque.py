# -*- coding: utf-8 -*-
"""
Gestion d'une bibliothèque en Python — Programmation Orientée Objet
Toutes les classes et le programme principal sont réunis dans ce fichier.
"""

from datetime import date


# ======================================================================
#  Classe Bibliothecaire
# ======================================================================
class Bibliothecaire:
    """Représente un bibliothécaire de la bibliothèque."""

    def __init__(self, nom, prenom, numero):
        self._nom = nom
        self._prenom = prenom
        self._numero = numero

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def numero(self):
        return self._numero

    def __str__(self):
        return f"Bibliothécaire n°{self._numero} | {self._prenom} {self._nom}"


# ======================================================================
#  Classe Conservateur
# ======================================================================
class Conservateur(Bibliothecaire):
    """Dirige la bibliothèque. Hérite de Bibliothécaire."""

    def __init__(self, nom, prenom, numero):
        Bibliothecaire.__init__(self, nom, prenom, numero)

    def __str__(self):
        return f"Conservateur n°{self._numero} | {self._prenom} {self._nom}"


# ======================================================================
#  Classe Emprunt
# ======================================================================
class Emprunt:
    """Représente l'emprunt d'un livre par un lecteur."""

    def __init__(self, livre, lecteur, date_emprunt=None):
        self._livre = livre
        self._lecteur = lecteur
        self._date_emprunt = date_emprunt if date_emprunt else date.today()
        self._date_retour = None

    @property
    def livre(self):
        return self._livre

    @property
    def lecteur(self):
        return self._lecteur

    @property
    def date_emprunt(self):
        return self._date_emprunt

    @property
    def date_retour(self):
        return self._date_retour

    def est_en_cours(self):
        return self._date_retour is None

    def enregistrer_retour(self, date_retour=None):
        self._date_retour = date_retour if date_retour else date.today()

    def __str__(self):
        statut = 'en cours' if self.est_en_cours() else f'rendu le {self._date_retour}'
        return (f"Emprunt | Livre n°{self._livre.numero} '{self._livre.titre}' | "
                f"Lecteur : {self._lecteur.prenom} {self._lecteur.nom} "
                f"(n°{self._lecteur.numero}) | "
                f"Emprunté le : {self._date_emprunt} | Statut : {statut}")


# ======================================================================
#  Classe Lecteur
# ======================================================================
class Lecteur:
    """Représente un lecteur inscrit dans la bibliothèque."""

    def __init__(self, nom, prenom, adresse, numero):
        self._nom = nom
        self._prenom = prenom
        self._adresse = adresse
        self._numero = numero
        self._emprunts = []

    @property
    def nom(self):
        return self._nom

    @property
    def prenom(self):
        return self._prenom

    @property
    def adresse(self):
        return self._adresse

    @property
    def numero(self):
        return self._numero

    @property
    def emprunts(self):
        return self._emprunts

    def ajouter_emprunt(self, emprunt):
        self._emprunts.append(emprunt)

    def retirer_emprunt(self, emprunt):
        if emprunt in self._emprunts:
            self._emprunts.remove(emprunt)

    def a_emprunt_en_cours(self):
        return len(self._emprunts) > 0

    def a_deja_emprunte(self, numero_livre):
        return any(e.livre.numero == numero_livre for e in self._emprunts)

    def __str__(self):
        nb = len(self._emprunts)
        livres = ', '.join(str(e.livre.numero) for e in self._emprunts) if nb else 'aucun'
        return (f"Lecteur n°{self._numero} | {self._prenom} {self._nom} | "
                f"{self._adresse} | Emprunts en cours : {nb} ({livres})")


# ======================================================================
#  Classe Livre
# ======================================================================
class Livre:
    """Représente un livre du fond documentaire."""

    def __init__(self, titre, auteur, numero, nb_exemplaires):
        self._titre = titre
        self._auteur = auteur
        self._numero = numero
        self._nb_exemplaires = nb_exemplaires
        self._nb_empruntes = 0

    @property
    def titre(self):
        return self._titre

    @property
    def auteur(self):
        return self._auteur

    @property
    def numero(self):
        return self._numero

    @property
    def nb_exemplaires(self):
        return self._nb_exemplaires

    @property
    def nb_disponibles(self):
        return self._nb_exemplaires - self._nb_empruntes

    @property
    def nb_empruntes(self):
        return self._nb_empruntes

    def est_disponible(self):
        return self.nb_disponibles > 0

    def emprunter(self):
        if not self.est_disponible():
            raise ValueError(f"Aucun exemplaire disponible pour '{self._titre}'.")
        self._nb_empruntes += 1

    def retourner(self):
        if self._nb_empruntes == 0:
            raise ValueError(f"Aucun exemplaire emprunté pour '{self._titre}'.")
        self._nb_empruntes -= 1

    def retirer_exemplaire(self):
        """Retire un exemplaire non emprunté. Retourne False si impossible."""
        if self.nb_disponibles == 0:
            return False
        self._nb_exemplaires -= 1
        return True

    def n_a_plus_d_exemplaire(self):
        return self._nb_exemplaires == 0

    def __str__(self):
        return (f"Livre n°{self._numero} | '{self._titre}' de {self._auteur} | "
                f"Exemplaires : {self._nb_exemplaires} total, "
                f"{self.nb_disponibles} disponible(s)")


# ======================================================================
#  Classe Bibliotheque
# ======================================================================
class Bibliotheque:
    """Gère le fond documentaire, les lecteurs, les bibliothécaires et les emprunts."""

    def __init__(self, nom, conservateur=None):
        self._nom = nom
        self._conservateur = conservateur
        self._lecteurs = []
        self._livres = []
        self._bibliothecaires = []
        self._emprunts = []

    # --- Propriétés ---
    @property
    def nom(self):
        return self._nom

    @property
    def conservateur(self):
        return self._conservateur

    @conservateur.setter
    def conservateur(self, c):
        self._conservateur = c

    # --- Gestion des lecteurs ---
    def ajout_lecteur(self, nom, prenom, adresse, numero):
        if self._trouver_lecteur_par_numero(numero) is not None:
            print(f"Erreur : un lecteur avec le numéro {numero} existe déjà.")
            return
        self._lecteurs.append(Lecteur(nom, prenom, adresse, numero))

    def chercher_lecteur_numero(self, numero):
        return self._trouver_lecteur_par_numero(numero)

    def chercher_lecteur_nom(self, nom, prenom):
        for l in self._lecteurs:
            if l.nom == nom and l.prenom == prenom:
                return l
        return None

    def retrait_lecteur(self, numero):
        lecteur = self._trouver_lecteur_par_numero(numero)
        if lecteur is None:
            print(f"Retrait lecteur : aucun lecteur avec le numéro {numero}.")
            return False
        if lecteur.a_emprunt_en_cours():
            return False
        self._lecteurs.remove(lecteur)
        return True

    def affiche_lecteurs(self):
        if not self._lecteurs:
            print("  Aucun lecteur enregistré.")
        for l in self._lecteurs:
            print(l)

    # --- Gestion des livres ---
    def ajout_livre(self, titre, auteur, numero, nb_exemplaires):
        if self._trouver_livre_par_numero(numero) is not None:
            print(f"Erreur : un livre avec le numéro {numero} existe déjà.")
            return
        self._livres.append(Livre(titre, auteur, numero, nb_exemplaires))

    def chercher_livre_numero(self, numero):
        return self._trouver_livre_par_numero(numero)

    def chercher_livre_titre(self, titre):
        for l in self._livres:
            if l.titre == titre:
                return l
        return None

    def retrait_livre(self, numero):
        livre = self._trouver_livre_par_numero(numero)
        if livre is None:
            print(f"Retrait livre : aucun livre avec le numéro {numero}.")
            return False
        if not livre.retirer_exemplaire():
            return False
        if livre.n_a_plus_d_exemplaire():
            self._livres.remove(livre)
        return True

    def affiche_livres(self):
        if not self._livres:
            print("  Aucun livre enregistré.")
        for l in self._livres:
            print(l)

    # --- Gestion des emprunts ---
    def emprunt_livre(self, numero_lecteur, numero_livre):
        lecteur = self._trouver_lecteur_par_numero(numero_lecteur)
        if lecteur is None:
            print(f"Emprunt impossible : lecteur n°{numero_lecteur} introuvable.")
            return
        livre = self._trouver_livre_par_numero(numero_livre)
        if livre is None:
            print(f"Emprunt impossible : livre n°{numero_livre} introuvable.")
            return
        if not livre.est_disponible():
            print(f"Emprunt impossible : aucun exemplaire disponible pour '{livre.titre}'.")
            return
        if lecteur.a_deja_emprunte(numero_livre):
            print(f"Emprunt impossible : {lecteur.prenom} {lecteur.nom} a déjà "
                  f"emprunté '{livre.titre}'.")
            return
        emprunt = Emprunt(livre, lecteur)
        livre.emprunter()
        lecteur.ajouter_emprunt(emprunt)
        self._emprunts.append(emprunt)
        print(f"Emprunt enregistré : '{livre.titre}' → {lecteur.prenom} {lecteur.nom}")

    def retour_livre(self, numero_lecteur, numero_livre):
        lecteur = self._trouver_lecteur_par_numero(numero_lecteur)
        if lecteur is None:
            print(f"Retour impossible : lecteur n°{numero_lecteur} introuvable.")
            return
        emprunt_cible = None
        for e in lecteur.emprunts:
            if e.livre.numero == numero_livre:
                emprunt_cible = e
                break
        if emprunt_cible is None:
            print(f"Retour impossible : le lecteur n°{numero_lecteur} n'a pas "
                  f"emprunté le livre n°{numero_livre}.")
            return
        emprunt_cible.enregistrer_retour()
        emprunt_cible.livre.retourner()
        lecteur.retirer_emprunt(emprunt_cible)
        print(f"Retour enregistré : '{emprunt_cible.livre.titre}' ← "
              f"{lecteur.prenom} {lecteur.nom}")

    def affiche_emprunts(self):
        if not self._emprunts:
            print("  Aucun emprunt enregistré.")
            return
        for e in self._emprunts:
            print(e)

    # --- Gestion des bibliothécaires ---
    def ajout_bibliothecaire(self, nom, prenom, numero):
        if self._trouver_bibliothecaire(numero) is not None:
            print(f"Erreur : bibliothécaire n°{numero} existe déjà.")
            return
        self._bibliothecaires.append(Bibliothecaire(nom, prenom, numero))

    def retrait_bibliothecaire(self, numero):
        bib = self._trouver_bibliothecaire(numero)
        if bib is None:
            return False
        self._bibliothecaires.remove(bib)
        return True

    def chercher_bibliothecaire(self, numero):
        return self._trouver_bibliothecaire(numero)

    def affiche_bibliothecaires(self):
        if self._conservateur:
            print(f"  Conservateur : {self._conservateur}")
        if not self._bibliothecaires:
            print("  Aucun bibliothécaire enregistré.")
        for b in self._bibliothecaires:
            print(f"  {b}")

    # --- Méthodes privées ---
    def _trouver_lecteur_par_numero(self, numero):
        for l in self._lecteurs:
            if l.numero == numero:
                return l
        return None

    def _trouver_livre_par_numero(self, numero):
        for l in self._livres:
            if l.numero == numero:
                return l
        return None

    def _trouver_bibliothecaire(self, numero):
        for b in self._bibliothecaires:
            if b.numero == numero:
                return b
        return None

    def __str__(self):
        return (f"Bibliothèque «{self._nom}» | "
                f"Lecteurs : {len(self._lecteurs)} | "
                f"Livres : {len(self._livres)} | "
                f"Emprunts totaux : {len(self._emprunts)}")


# ======================================================================
#  Programme principal
# ======================================================================
if __name__ == '__main__':

    # Creation d'une bibliotheque
    b = Bibliotheque('Bibliotheque ECL')

    # Ajout de lecteurs
    b.ajout_lecteur('Duval','Pierre','rue de la Paix',1)
    b.ajout_lecteur('Dupond','Laurent','rue de la Gare',2)
    b.ajout_lecteur('Martin','Marie','rue La Fayette',3)
    b.ajout_lecteur('Dubois','Sophie','rue du Stade',4)

    # Ajout de livres
    b.ajout_livre('Le Pere Goriot','Honore de Balzac',101,2)
    b.ajout_livre('Les Hauts de Hurlevent','Emilie Bronte',102,2)
    b.ajout_livre('Le Petit Prince','Antoine de Saint Exupery',103,2)
    b.ajout_livre("L'Etranger",'Albert Camus',104,2)

    # Affichage des lecteurs et des livres
    print('\n--- Liste des lecteurs :')
    print('-------------------------------')
    b.affiche_lecteurs()
    print('\n--- Liste des livres :')
    print('-------------------------------')
    b.affiche_livres()

    # Recherches de lecteurs par numero
    print('\n--- Recherche de lecteurs :')
    print('-------------------------------')
    lect = b.chercher_lecteur_numero(1)
    if lect != None:
        print(lect)
    else:
        print('Lecteur non trouve')

    lect = b.chercher_lecteur_numero(6)
    if lect != None:
        print(lect)
    else:
        print('Lecteur non trouve')

    # Recherches de lecteurs par nom
    lect = b.chercher_lecteur_nom('Martin','Marie')
    if lect != None:
        print(lect)
    else:
        print('Lecteur non trouve')

    lect = b.chercher_lecteur_nom('Le Grand','Paul')
    if lect != None:
        print(lect)
    else:
        print('Lecteur non trouve')

    # Recherches de livres par numero
    print('\n--- Recherche de livres :')
    print('-------------------------------')
    livre = b.chercher_livre_numero(101)
    if livre != None:
        print('Livre trouve :',livre)
    else:
        print('Livre non trouve')

    livre = b.chercher_livre_numero(106)
    if livre != None:
        print('Livre trouve :',livre)
    else:
        print('Livre non trouve')

    # Recherches de livres par titre
    livre = b.chercher_livre_titre('Les Hauts de Hurlevent')
    if livre != None:
        print('Livre trouve :',livre)
    else:
        print('Livre non trouve')

    livre = b.chercher_livre_titre('Madame Bovarie')
    if livre != None:
        print('Livre trouve :',livre)
    else:
        print('Livre non trouve')

    # Quelques emprunts
    print('\n--- Quelques emprunts :')
    print('-------------------------------')
    b.emprunt_livre(1,101)
    b.emprunt_livre(1,104)
    b.emprunt_livre(2,101)
    b.emprunt_livre(2,105)
    b.emprunt_livre(3,101)
    b.emprunt_livre(3,104)
    b.emprunt_livre(4,102)
    b.emprunt_livre(4,103)

    # Affichage des emprunts, des lecteurs et des livres
    print('\n--- Liste des emprunts :')
    print('-------------------------------')
    b.affiche_emprunts()
    print('\n--- Liste des lecteurs :')
    print('-------------------------------')
    b.affiche_lecteurs()
    print('\n--- Liste des livres :')
    print('-------------------------------')
    b.affiche_livres()

    # Quelques retours de livres
    print('\n--- Quelques retours de livres :')
    print('-------------------------------')
    b.retour_livre(1,101)
    b.retour_livre(1,102)
    b.retour_livre(3,104)
    b.retour_livre(10,108)

    # Affichage des emprunts, des lecteurs et des livres
    print('\n--- Liste des emprunts :')
    print('-------------------------------')
    b.affiche_emprunts()
    print('\n--- Liste des lecteurs :')
    print('-------------------------------')
    b.affiche_lecteurs()
    print('\n--- Liste des livres :')
    print('-------------------------------')
    b.affiche_livres()

    # Suppression de quelques livres
    rep = b.retrait_livre(101)
    if not rep:
        print('Retrait du livre impossible')
    else:
        print('Retrait du livre effectue')

    b.retour_livre(2,101)

    rep = b.retrait_livre(101)
    if not rep:
        print('Retrait du livre impossible')
    else:
        print('Retrait du livre effectue')

    # Suppression de quelques lecteurs
    rep = b.retrait_lecteur(1)
    if not rep:
        print('Retrait du lecteur impossible')
    else:
        print('Retrait du lecteur effectue')

    b.retour_livre(1,104)

    rep = b.retrait_lecteur(1)
    if not rep:
        print('Retrait du lecteur impossible')
    else:
        print('Retrait du lecteur effectue')

    # Affichage final
    print('\n--- Liste des emprunts :')
    print('-------------------------------')
    b.affiche_emprunts()
    print('\n--- Liste des lecteurs :')
    print('-------------------------------')
    b.affiche_lecteurs()
    print('\n--- Liste des livres :')
    print('-------------------------------')
    b.affiche_livres()
