from operator import index
from colorama import Fore, Style, init
from tkinter import *
from random import *
init()
LB = Fore.LIGHTBLACK_EX
Reset = Style.RESET_ALL

# fenetre = Tk()
#
#
# label = Label(fenetre, text="Hello World")
# label.pack()
# # bouton de sortie
# bouton=Button(fenetre, text="Fermer", command=fenetre.quit)
# bouton.pack()
#
# fenetre.mainloop()


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.cartes = []
        self.jetons = 1000
        self.victoires = 0
        self.mise = 0
        self.fold = False
    def recevoir_carte(self, carte):
        self.cartes.append(carte)


    def afficher_cartes(self):
        for x in range(len(self.cartes)):
            carte = self.cartes[x]
            if "P" in carte:
                couleur = "♠"
            elif "C" in carte:
                couleur = "♥"
            elif "T" in carte:
                couleur = "♣"
            elif "K" in carte:
                couleur = "♦"
            carte = carte.replace("P","").replace("C","").replace("T","").replace("K","")
            carte = carte.replace("1","As")
            carte = carte.replace("v","Valet")
            carte = carte.replace("d","Dame")
            carte = carte.replace("r","Roi")

            print(carte,"de",couleur, end="")
            if x < len(self.cartes)-1:
                print(" | ",end="")
        print("\n\n")


    def decision(self,joueur,robots,partie):
        if joueur:
            if robots[-0].mise == 0:
                choix = input("Check / Bet / Fold  -->  ").lower()
                if "check" in choix:
                    pass
                elif "bet" in choix:
                    while True:
                        try:
                            mise = int(input("Montant : "))
                            if mise > 0:  # Vérifie que le montant est positif
                                break  # Sort de la boucle si l'entrée est valide
                            else:
                                print("Le montant doit être supérieur à 0.")
                        except ValueError:
                            print("Veuillez entrer un nombre valide.")
                    partie.pot += mise
                    self.jetons -= mise
                    print(f" #-- Vous misez {mise} jetons.\n --- Il vous reste {self.jetons} jetons.")
                elif "fold" in choix:
                    self.fold = True
                    print(" #-- Vous vous couchez.")
                else:
                    print("Entrée invalide")
                    choix = input("Check / Bet / Fold  -->  ").lower()
            else:
                choix = input("Bet / Raise / Fold  -->  ").lower()

pass

class JeuDeCartes:
    def __init__(self):
        self.cartes = [
            "1P", "2P", "3P", "4P", "5P", "6P", "7P", "8P", "9P", "10P", "vP", "dP", "rP",  # Pique
            "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "vC", "dC", "rC",  # Cœur
            "1T", "2T", "3T", "4T", "5T", "6T", "7T", "8T", "9T", "10T", "vT", "dT", "rT",  # Trèfle
            "1K", "2K", "3K", "4K", "5K", "6K", "7K", "8K", "9K", "10K", "vK", "dK", "rK"   # Carreau
        ]
    def retirer_carte(self, carte):
        self.cartes.remove(carte)


class Partie:
    def __init__(self, joueur, robots):
        self.joueur = joueur
        self.robots = robots
        self.jeu_de_cartes = JeuDeCartes()
        self.blind = randint(0,len(robots))
        self.pot = 0
        self.ordre = [joueur] + robots

    def reset(self,robots):
        # Réinitialise le jeu de cartes
        self.jeu_de_cartes = JeuDeCartes()
        self.blind = randint(0,len(robots))
        self.pot = 0

        # Réinitialise les mains des joueurs
        self.joueur.cartes = []
        for robot in self.robots:
            robot.cartes = []

    def distribuer_cartes(self,joueur,robots,jeu_de_carte):
        for _ in range(2):
            nCarte = randint(0,len(jeu_de_carte.cartes)-1)
            carte = jeu_de_carte.cartes[nCarte]
            joueur.recevoir_carte(jeu_de_carte.cartes[nCarte])
            jeu_de_carte.retirer_carte(carte)
            for robot in robots:
                nCarte = randint(0,len(jeu_de_carte.cartes)-1)
                carte = jeu_de_carte.cartes[nCarte]
                robot.recevoir_carte(jeu_de_carte.cartes[nCarte])
                jeu_de_carte.retirer_carte(carte)

    def afficher_table(self,joueur, robots):
        nb_robots = len(robots)
        # Nombre total de places autour de la table (en haut)
        places = nb_robots

        # Création d'une ligne de séparation
        if robots[0].fold:
            print(f"{LB}+---------{Reset}",end="")
        else:
            print("+---------",end="")
        for i in range(1,len(robots)):
            if robots[i].fold:
                if robots[i-1].fold:
                    print(f"{LB}+---------{Reset}",end="")
                else:
                    print(f"+{LB}---------{Reset}",end="")
            else:
                print(f"+---------",end="")
        if robots[-1].fold:
            print(f"{LB}+{Reset}")
        else:
            print("+")

        # Afficher les robots en haut de la table
        for i in range(nb_robots):
            if robots[i].fold:
                if i == 0:
                    print(f"{LB}| {robots[i].nom:<3} {Reset}", end="")
                else:
                    if robots[i-1].fold:
                        print(f"{LB}| {robots[i].nom:<3} {Reset}", end="")
                    else:
                        print(f"| {LB}{robots[i].nom:<3} {Reset}", end="")
            else:
                if i == 0:
                    print(f"| {robots[i].nom:<3} ", end="")
                else:
                    print(f"| {robots[i].nom:<3} ", end="")

        # Fin de la ligne de robots
        if robots[len(robots)-1].fold:
            print(f"{LB}|{Reset}")
        else:
            print("|")

        # Création d'une ligne de séparation
        if robots[0].fold:
            print(f"{LB}+---------{Reset}",end="")
        else:
            print("+---------",end="")
        for i in range(1,len(robots)):
            if robots[i].fold:
                if robots[i-1].fold:
                    print(f"{LB}+---------{Reset}",end="")
                else:
                    print(f"+{LB}---------{Reset}",end="")
            else:
                print(f"+---------",end="")
        if robots[-1].fold:
            print(f"{LB}+{Reset}")
        else:
            print("+")

        if joueur.fold:
            # Afficher le joueur au centre en bas
            print(LB+" " + " " * int((((1 + 10 * places)-len(joueur.nom)-8) / 2)),f"| {joueur.nom:<3} |")
            # Ligne de séparation finale
            print(" " + " " * int((((1 + 10 * places)-len(joueur.nom)-4) / 2)), end="\b")
            print("+" + "-" * len(joueur.nom) + "--" + "+\n"+Reset)
        else:
            # Afficher le joueur au centre en bas
            print(" " + " " * int((((1 + 10 * places)-len(joueur.nom)-8) / 2)),f"| {joueur.nom:<3} |")
            # Ligne de séparation finale
            print(" " + " " * int((((1 + 10 * places)-len(joueur.nom)-4) / 2)), end="\b")
            print("+" + "-" * len(joueur.nom) + "--" + "+\n")

    def tourner_blind(self, robots):
        if self.blind == len(robots):
            self.blind = 0
        else:
            self.blind += 1

class Jeu:
    print("\n\n\n\n\n\n")
    # nom_du_joueur = input("Nom du joueur : ")
    nom_du_joueur = "Noé"
    # nb_robots = int(input("Nombre de robots : "))
    nb_robots = 5

    joueur = Joueur(nom_du_joueur)
    robots = [Joueur(f"Robot {x}") for x in range(nb_robots)]
    jeu_de_cartes = JeuDeCartes()

    while True:
        # Création et initialisation d'une nouvelle partie
        partie = Partie(joueur, robots)
        partie.reset(robots)
        # Distribution des cartes
        partie.distribuer_cartes(joueur,robots,jeu_de_cartes)

        # Afficher la table
        print("              -------- Table -------- \n")
        partie.afficher_table(joueur,robots)
        print("              ------ Vos Cartes ------ \n")
        joueur.afficher_cartes()
        # Prendre décision
        if partie.blind == 0:
            joueur.decision(True, robots, partie)
        else:
            robots[partie.blind - 1].decision(False, robots, partie)

        # Logique de la partie ici (mise, tours de jeu, etc.)
        break  # Juste pour arrêter la boucle infinie après une partie dans cet exemple


