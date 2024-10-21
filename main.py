from tkinter import *
from random import *

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
    def recevoir_carte(self, carte):
        self.cartes.append(carte)


    def afficher_cartes(self):
        for x in range(len(self.cartes)):
            print(self.cartes[x],end=" ")


    def décision(self):
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

    def reset(self):
        # Réinitialise le jeu de cartes
        self.jeu_de_cartes = JeuDeCartes()

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
        print("+" + "---------+" * places)

        # Afficher les robots en haut de la table
        for i in range(nb_robots):
            if i == 0:
                print(f"| {robots[i].nom:<3} ", end="")
            else:
                print(f"| {robots[i].nom:<3} ", end="")
        print("|")  # Fin de la ligne de robots

        # Ligne de séparation
        print("+" + "---------+" * places)

        # Afficher le joueur au centre en bas
        print(" " * int((((1 + 10 * places)-len(joueur.nom)-8) / 2)),f"| {joueur.nom:<3} |")

        # Ligne de séparation finale
        print(" " * int((((1 + 10 * places)-len(joueur.nom)-4) / 2)), end="\b")
        print("+" + "-" * len(joueur.nom) + "--" + "+")


class Jeu:
    print("\n\n\n\n\n\n")
    # nom_du_joueur = input("Nom du joueur : ")
    nom_du_joueur = "Noé"
    # nb_robots = int(input("Nombre de robots : "))
    nb_robots = 3

    joueur = Joueur(nom_du_joueur)
    robots = [Joueur(f"Robot {x}") for x in range(nb_robots)]
    jeu_de_cartes = JeuDeCartes()

    while True:
        # Création et initialisation d'une nouvelle partie
        partie = Partie(joueur, robots)
        partie.reset()
        # Distribution des cartes
        partie.distribuer_cartes(joueur,robots,jeu_de_cartes)

        # Afficher la table
        print(" -------- Table -------- \n")
        partie.afficher_table(joueur,robots)
        print(" ------ Vos Cartes ------ \n")
        joueur.afficher_cartes()


        # Logique de la partie ici (mise, tours de jeu, etc.)
        break  # Juste pour arrêter la boucle infinie après une partie dans cet exemple


