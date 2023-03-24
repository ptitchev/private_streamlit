import numpy as np

#1 : Evenement (a mettre en JSON)

L_nom = np.array(["Fumer une cigarette",
         "Rouler un joint", 
         "Fumer un Blunt ", 
         "Dose de champy", 
         "Parachute de MD", 
         "Extasy", 
         "Poppers", 
         "Déguster un cigare", 
         "Boire une bière",
         "Verre d'alcool fort", 
         "Se servir un vrai verre", 
         "1 shot", 
         "2 shots", 
         "3 shots", 
         "Cul sec", 
         "Préparer des coktails", 
         "Jeu d'alcool", 
         "Vrai jeu d'alcool", 
         "BeerPong", 
         "Danser", 
         "Danser au rythme endiablé de la musique", 
         "Sociabiliser", 
         "Enflammer le dansefloor", 
         "Faire des blagues"])

L_params = ['temps', 'BPM', 'energie', 'alcool', 'drogue', 'faim', 'fun']

L_choix = np.array([[5, 0, 0, -1, 0, 0, 0], 
                    [20, -1, -1, 0, 2, -1, 0], 
                    [32, -1, -2, 0, 3, 0, 1], 
                    [70, 2, 1, 0, 3, -1, -1], 
                    [90, 3, 2, 0, 4, -3, 2], 
                    [90, 3, 4, 0, 4, -4, 1], 
                    [5, 2, 1, 0, 1, 0, 1], 
                    [45, 0, 0, -3, 0, 0, 1], 
                    [8, 0, 0, 1, 0, 0, 1], 
                    [13, 0, 0, 2, 0, 0, 0], 
                    [22, 1, -1, 4, 0, -1, 2], 
                    [2, 1, 0, 1, 0, 0, 0], 
                    [3, 1, 0, 2, 0, 0, 0], 
                    [4, 2, 0, 3, 0, 0, 3], 
                    [5, 1, 0, 4, 0, 0, 1], 
                    [20, -1, -1, 2, -1, 0, -2], 
                    [17, -1, 0, 2, 0, 0, 2], 
                    [28, -1, -1, 3, 0, -1, 3], 
                    [41, -1, -1, 1, 0, 0, 2], 
                    [22, 1, -1, -1, -1, 0, 1], 
                    [36, 2, -2, -2, -1, -1, 2], 
                    [32, -1, 0, -1, 0, 0, -1], 
                    [17, 2, -1, -1, -1, -1, 4], 
                    [21, -1, 0, 0, 0, 0, 2]])

nb_choix = len(L_nom)

#2 : Mort et ev (a faire)
lims = np.array([[0, 40, 0, 0, 0, 0, 0],[720, 165, 10, 10, 10, 10, 10]])

#3 : Game et derrivées
game = np.zeros(16)

etat = np.array([0, 0, 80, 8, 0, 0, 5, 0])
depassements = np.zeros(7)

game[0:8] += game[0:8] + etat
game[8:15] += depassements