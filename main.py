from operator import index
from colorama import Fore, Style, init
from tkinter import *
from random import *
from collections import Counter
import re
init()
LB = Fore.LIGHTBLACK_EX
Reset = Style.RESET_ALL
RB = "\033[41m"
BB = "\033[40m"
Bold = "\033[1m"
ResetBold = "\033[22m"

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

    def remove_cartes(self):
        self.cartes = []

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
            carte = carte.replace("1","1" if "10" in carte else "As")
            carte = carte.replace("v","Valet")
            carte = carte.replace("d","Dame")
            carte = carte.replace("r","Roi")

            print((RB if (couleur == "♥" or couleur == "♦") else BB),carte,"de",Bold+couleur,Reset, end="")
            if x < len(self.cartes)-1:
                print(" | ",end="")
        print("\n\n")


    def decision(self,joueur,robots,partie,jeu_de_cartes):
        if joueur:
            if partie.mise_minimale == 0:
                choix = input("Check / Bet / Fold  -->  ").lower()
                if "check" in choix:
                    pass
                for car in choix:
                    if car.isdigit(): return True
                if "bet" in choix:
                    while True:
                        try:
                            mise = int(input("Montant : "))
                            if mise > 0:  # Vérifie que le montant est positif
                                break  # Sort de la boucle si l'entrée est valide
                            elif mise < partie.mise_minimale:
                                print("Le montant doit être supérieur à la dernière mise.")
                            else:
                                print("Le montant doit être supérieur à 0.")
                        except ValueError:
                            print("Veuillez entrer un nombre valide.")
                    partie.pot += mise
                    self.jetons -= mise
                    partie.mise_minimale = mise
                    print(f" #-- Vous misez {mise} jetons.\n --- Il vous reste {self.jetons} jetons.")
                elif "fold" in choix:
                    self.fold = True
                    print(" #-- Vous vous couchez.")
                else:
                    print("Entrée invalide")
                    choix = input("Check / Bet / Fold  -->  ").lower()
            elif self.jetons < partie.mise_minimale:
                choix = input("All-in / Fold  -->  ").lower()
            else:
                choix = input("Bet / Raise / Fold  -->  ").lower()
        else:
            self._decision_robot(robots,partie,jeu_de_cartes)

    def _decision_robot(self,robots,partie,jeu_de_cartes):
        if not self.fold:
            # if self.jetons < partie.mise_minimale:
            #     pass # All-in ou fold
            # else:
            #     if len(partie.table) == 0:
            #         if -3 < (jeu_de_cartes.numero(self.cartes[0])-jeu_de_cartes.numero(self.cartes[1])) < 3:
            #             pb = randint(1,100)
            #             if pb > 70:
            #                 result = 0 # Mise à mettre
            #         if jeu_de_cartes.couleur(self.cartes[0]) == jeu_de_cartes.couleur(self.cartes[1]):
            #             pb = randint(1,100)
            #             if pb > 50:
            #                 result = 0 # Mise à mettre
            #         else:
            #             pb = randint(1,100)
            #             if pb > 85:
            #                 result = 0 # Mise à mettre
            #     elif len(partie.table) == 3:
            #         if max(Counter([self.cartes[0],self.cartes[1],partie.table[0],partie.table[1],partie.table[2]]).values()) >= 4:
            #             pb = randint(1,100)
            #             if pb > 10:
            #                 result = 0 # Mise à mettre
            #         elif max(Counter([self.cartes[0],self.cartes[1],partie.table[0],partie.table[1],partie.table[2]]).values()) > 3:
            #             pb = randint(1,100)
            #             if pb > 25:
            #                 result = 0 # Mise à mettre
            #     elif len(partie.table) == 4:
            #         if max(Counter([self.cartes[0],self.cartes[1],partie.table[0],partie.table[1],partie.table[2],partie.table[3]]).values()) > 4:
            #             pb = randint(1,100)
            #             if pb > 10:
            #                 result = 0 # Mise à mettre
            #         elif max(Counter([self.cartes[0],self.cartes[1],partie.table[0],partie.table[1],partie.table[2],partie.table[3]]).values()) > 3:
            #             pb = randint(1,100)
            #             if pb > 25:
            #                 result = 0 # Mise à mettre

            """
            Cette méthode gère la prise de décision pour un robot en fonction du nombre de cartes sur la table,
            de la force de sa main, et des probabilités de checker ou miser.
            """
            result = None  # Variable qui définira la mise finale du robot
            cartes = [self.cartes[0], self.cartes[1]] + partie.table  # Fusion des cartes du robot et celles de la table

            # Probabilité de check ou de miser
            prob_check = 0  # Probabilité de check
            prob_miser_petit = 0  # Probabilité de miser petit
            prob_miser_gros = 0  # Probabilité de miser gros

            # Étape pré-flop (aucune carte sur la table)
            if len(partie.table) == 0:
                if -3 < (jeu_de_cartes.numero(self.cartes[0]) - jeu_de_cartes.numero(self.cartes[1])) < 3:
                    prob_check = 30
                    prob_miser_petit = 50
                    prob_miser_gros = 20
                elif jeu_de_cartes.couleur(self.cartes[0]) == jeu_de_cartes.couleur(self.cartes[1]):
                    prob_check = 20
                    prob_miser_petit = 40
                    prob_miser_gros = 40
                else:
                    prob_check = 15
                    prob_miser_petit = 55
                    prob_miser_gros = 30

            # Étape du flop (3 cartes sur la table)
            elif len(partie.table) == 3:
                occurrences = Counter(cartes).values()
                if max(occurrences) >= 4:  # Si le robot a un carré
                    prob_check = 10
                    prob_miser_petit = 30
                    prob_miser_gros = 60
                elif max(occurrences) > 3:  # Si le robot a un brelan
                    prob_check = 20
                    prob_miser_petit = 40
                    prob_miser_gros = 40
                else:
                    prob_check = 35
                    prob_miser_petit = 50
                    prob_miser_gros = 15

            # Étape du turn (4 cartes sur la table)
            elif len(partie.table) == 4:
                occurrences = Counter(cartes).values()
                if max(occurrences) > 4:  # Si le robot a un carré ou mieux
                    prob_check = 5
                    prob_miser_petit = 25
                    prob_miser_gros = 70
                elif max(occurrences) > 3:  # Si le robot a un brelan
                    prob_check = 20
                    prob_miser_petit = 45
                    prob_miser_gros = 35
                else:
                    prob_check = 30
                    prob_miser_petit = 50
                    prob_miser_gros = 20

            # Étape de la river (5 cartes sur la table)
            elif len(partie.table) == 5:
                occurrences = Counter(cartes).values()
                if max(occurrences) > 4:  # Si le robot a un carré
                    prob_check = 5
                    prob_miser_petit = 20
                    prob_miser_gros = 75
                elif max(occurrences) > 3:  # Si le robot a un brelan
                    prob_check = 20
                    prob_miser_petit = 40
                    prob_miser_gros = 40
                else:
                    prob_check = 30
                    prob_miser_petit = 50
                    prob_miser_gros = 20

            # Choix entre check, miser petit ou miser gros en fonction des probabilités
            decision = randint(1, 100)
            if decision <= prob_check:
                result = 0  # Le robot décide de checker
            elif decision <= prob_check + prob_miser_petit:
                result = randint(10, 50)  # Mise entre 10 et 50 jetons
            else:
                result = randint(51, min(self.jetons, 200))  # Mise entre 51 et 200 jetons, mais pas plus que les jetons restants

            # Si la mise est inférieure à la mise minimale
            if result < partie.mise_minimale:
                decision_coucher = randint(1, 100)
                if decision_coucher <= 10:  # Faible probabilité de se coucher (10%)
                    self.fold = True
                    print(f"{self.nom} décide de se coucher.")
                    return
                else:  # Forte probabilité de rechoisir une mise (90%)
                    result = max(partie.mise_minimale, randint(10, min(self.jetons, 200)))
                    print(f"{self.nom} réajuste sa mise à {result} jetons.")

            # Appliquer la mise ou le check
            if result == 0:
                print(f"{self.nom} Check.")
            else:
                partie.pot += result
                self.jetons -= result
                partie.mise_minimale = result
                print(f"{self.nom} Bet {result} jetons.")



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

    def couleur(self,carte):
        carte = re.sub(r'\d+', '', carte)
        return carte
    def numero(self,carte):
        carte = carte.replace("P","").replace("C","").replace("T","").replace("K","").replace("v","11").replace("d","12").replace("r","13")
        return int(carte)


class Partie:
    def __init__(self, joueur, robots):
        self.joueur = joueur
        self.robots = robots
        self.jeu_de_cartes = JeuDeCartes()
        self.blind = randint(0,len(robots))
        self.pot = 0
        self.ordre = [joueur] + robots
        self.table = []
        self.mise_minimale = 0

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

    def afficher_cartes(self):
        for x in range(len(self.table)):
            carte = self.table[x]
            if "P" in carte:
                couleur = "♠"
            elif "C" in carte:
                couleur = "♥"
            elif "T" in carte:
                couleur = "♣"
            elif "K" in carte:
                couleur = "♦"
            carte = carte.replace("P","").replace("C","").replace("T","").replace("K","")
            carte = carte.replace("1","1" if "10" in carte else "As")
            carte = carte.replace("v","Valet")
            carte = carte.replace("d","Dame")
            carte = carte.replace("r","Roi")

            texte = f"{carte} de {couleur}"
            print(f"{RB if (couleur == "♥" or couleur == "♦") else BB}{Bold}{(texte):^10}{Reset}", end="")
            if x < len(self.table)-1:
                print(" | ",end="")

    def tourner_blind(self, robots):
        if self.blind == len(robots):
            self.blind = 0
        else:
            self.blind += 1

    def flop(self,jeu_de_cartes):
        for i in range(3):
            carte = jeu_de_cartes.cartes[randint(0,len(jeu_de_cartes.cartes)-1)]
            self.table.append(carte)
            jeu_de_cartes.cartes.remove(carte)

    def turn_river(self,jeu_de_cartes):
        carte = jeu_de_cartes.cartes[randint(0,len(jeu_de_cartes.cartes)-1)]
        self.table.append(carte)
        jeu_de_cartes.cartes.remove(carte)


class Jeu:
    print("\n\n\n\n\n\n")

    def mise(self,joueur,robots,partie,jeu_de_cartes):
        for i in range(len(robots)):
            # Ajustement pour ne pas dépasser la taille des robots
            index = (partie.blind + i) % len(robots)  # Utilise le modulo pour gérer le dépassement
            print(robots[index].nom, robots[index].cartes)
            if index == partie.blind:  # Si c'est au tour du joueur avec la blind
                joueur.decision(True, robots, partie, jeu_de_cartes)
            else:
                robots[index].decision(False, robots, partie, jeu_de_cartes)
            print(robots[index].jetons)

    def jeu(self,joueur,robots,jeu_de_cartes):
        while True:
            # Création et initialisation d'une nouvelle partie
            partie = Partie(joueur, robots)
            partie.reset(robots)
            # Distribution des cartes
            partie.distribuer_cartes(joueur,robots,jeu_de_cartes)

            # Afficher la table
            print("              -----------------------\n              ------- Joueurs ------- \n              -----------------------\n")
            partie.afficher_table(joueur,robots)
            print("              -----------------------\n              ------ Vos Cartes ----- \n              -----------------------\n")
            joueur.afficher_cartes()

            while not joueur.fold:
                couche = 0
                for robot in robots:
                    if robot.fold:
                        couche += 1
                if couche == len(robots):
                    break

                # Pré-flop
                self.mise(joueur, robots, partie, jeu_de_cartes)

                # Flop
                partie.flop(jeu_de_cartes)
                print("              -----------------------\n              -------- Table --------              \n              -----------------------\n")
                partie.afficher_cartes()
                print("\n--------------- Flop ---------------\n\n")
                self.mise(joueur, robots, partie, jeu_de_cartes)

                print("              -----------------------\n              ------- Joueurs ------- \n              -----------------------\n")
                partie.afficher_table(joueur,robots)
                print("              -----------------------\n              ------ Vos Cartes ----- \n              -----------------------\n")
                joueur.afficher_cartes()

                # Turn
                partie.turn_river(jeu_de_cartes)
                print("              -----------------------\n              -------- Table --------              \n              -----------------------\n")
                partie.afficher_cartes()
                print("\n--------------- Flop --------------- + -- Turn -- \n\n")
                self.mise(joueur, robots, partie, jeu_de_cartes)

                # Afficher la table
                print("              -----------------------\n              ------- Joueurs ------- \n              -----------------------\n")
                partie.afficher_table(joueur,robots)
                print("              -----------------------\n              ------ Vos Cartes ----- \n              -----------------------\n")
                joueur.afficher_cartes()

                # River
                partie.turn_river(jeu_de_cartes)
                print("              -----------------------\n              -------- Table --------              \n              -----------------------\n")
                partie.afficher_cartes()
                print("\n--------------- Flop --------------- + -- Turn -- + -- River --\n\n")
                self.mise(joueur, robots, partie, jeu_de_cartes)

                break

            break




jeu = Jeu()
# nom_du_joueur = input("Nom du joueur : ")
nom_du_joueur = "Noé"
# nb_robots = int(input("Nombre de robots : "))
nb_robots = 5

joueur = Joueur(nom_du_joueur)
robots = [Joueur(f"Robot {x}") for x in range(nb_robots)]
jeu_de_cartes = JeuDeCartes()
jeu.jeu(joueur,robots,jeu_de_cartes)
