import numpy as np
import json
import random
#import numba
#from numba import jit

#1: gestion de l'etat

with open("ev.json", 'r') as f:
    data = json.load(f)
L_nom = np.array(data['index'])
L_params = np.array(data['columns'])
L_choix = np.array(data['data'])
nb_choix = len(L_nom)

#2 : Mort et ev (a faire)

with open("lims.json", 'r') as f:
    data = json.load(f)
lims = np.array(data["data"]).T

L_death = ["Tu n'as pas dormi de la soirée, ce qui t'as vidé de ton âme. Tu es devenu un zombie", 
           "Tu t'es gavé toute la soirée. Tu est mort d'une indigestion tel le gros porc que tu es",
           "Tu t'es un peu trop drogué ce soir. Une overdose est si vite arrivé",
           "Tu n'as pas été très fun ce soir. Tu as été exclue de la soirée",
           "Ton foix n'as pas tenu le rythme imposé ce soir. Durant ton comas éthylique personne n'était assez sobre pour s'occuper de toi",
           "Trop confiant et trop bourré, tu as brillamment escaladé un arbre. En descendant tu es tombé. Le plus important c'est pas la chute, c'est l'atterrissage (mortel)",
           "Tu as été pris d'allucinations en confondant un cailloux avec une saucisse. Un repas mortel",
           "Ton coeur a laché, c'est triste une crise cardiaque si jeune",
           "Tout le monde avait trop faim ce soir, tu t'es fait dévoré par un autre qui avait plus faim que toi"]

#3 : Game et derrivées
game = np.zeros(16)

etat = np.array([0, 0, 80, 8, 0, 0, 5, 0])
depassements = np.zeros(7)

game[0:8] += game[0:8] + etat
game[8:15] += depassements

import pandas as pd
data_choix = pd.DataFrame(L_choix, index = L_nom, columns = L_params)
data_lims = pd.DataFrame(lims.T, index = L_params, columns = ['-', '+'])

#@numba.njit
def add_environ(param, to_add):
  if to_add >= 0 :
    dec = round((to_add+5)/10)
    dec = random.randint(0, 2 * dec) - dec
  else :
    dec = round((to_add-5)/10)
    dec = random.randint(2 * dec, 0) - dec
  return param + to_add + dec

#@numba.njit
def add_BPM(BPM, to_add):
  dec = round((BPM)/10)
  dec = to_add * random.randint(0, dec)
  return BPM + dec

#@numba.njit
def update_etat(etat, choix):
  etat[1] = add_environ(etat[1], choix[0])
  etat[2] = add_BPM(etat[2], choix[1])
  for i in range(5):
    etat[i + 3] = add_environ(etat[i + 3], choix[i + 2])
  #return etat


#2: gestion des dépassements

#@numba.njit
def lim_haut(etat, col, lim):
  if etat[col] > lim:
    etat[col] = lim
    return True
  return False

#@numba.njit
def lim_bas(etat, col, lim):
  if etat[col] < lim:
    etat[col] = lim
    return True
  return False

#@numba.njit
def check_etat(etat, depassements, lims = lims):
  for i in range(7):
    if lim_bas(etat, i+1, lims[0][i]):
      depassements[i] += -1
    if lim_haut(etat, i+1, lims[1][i]):
      depassements[i] += 1


#3: Gestion des condition de mort

#@numba.njit
def D_Zombie(depassements):
  if depassements[0] > 0:
    return True
  return False

def D_Indigestion(depassements):
  if depassements[5] > 1:
    return True
  return False

#def D_Surplut() 3 vomis

#def D_Volant() mort au volant

def D_Overdosed(depassements):
  if depassements[4] > 1:
    return True
  return False

def D_Exclue(depassements):
  if depassements[6] < -1:
    return True
  return False

#def fou() danser au rythme endiablée avec drogue eleve

def D_ethylique(depassements):
  if depassements[3] > 2:
    return True
  return False

def D_confiant(depassements):
  if (depassements[6] > 1) and (depassements[3] > 0) :
    return True
  return False

def D_allutination(depassements):
  if (depassements[4] < 0) and (depassements[5]> 2 ):
    return True
  return False

def D_cardiaque(depassements):
  if (depassements[1] > 1) or (depassements[1]< 0 ) or (depassements[2] > 0):
    return True
  return False

def D_affame(depassements):
  if depassements[5] < -2 :
    return True
  return False
  
#@numba.njit
def check_dead(depassements):
  if D_Zombie(depassements):
    return 1 #, "Tu n'as pas dormi de la soirée, ce qui t'as vidé de ton âme. Tu es devenu un zombie"]
  if D_Indigestion(depassements):
    return 2
  if D_Overdosed(depassements):
    return 3
  if D_Exclue(depassements):
    return 4
  if D_ethylique(depassements):
    return 5
  if D_confiant(depassements):
    return 6
  if D_allutination(depassements):
    return 7
  if D_cardiaque(depassements):
    return 8
  if D_affame(depassements):
    return 9
  
  return 0


#4: Gestion du selecteur de choix futur

#@numba.njit
def send_choix(nb = nb_choix):
  a = random.randint(0,nb-1)
  b = random.randint(0, nb-1)
  while b == a:
    b = random.randint(0, nb-1)
  c = random.randint(0, nb-1)
  while (c == a) or (c == b):
    c = random.randint(0, nb-1)

  return np.array([a, b, c])

#5: Jouer un tour

#@numba.njit
def play_turn(game, choix = np.zeros(1)):
  if len(choix) > 1:
    game[-1] += 1
    update_etat(game[0:8], choix)
    check_etat(game[0:8], game[8:15])
    death = check_dead(game[8:15])
    if death > 0:
      game[0] = 1
      return np.array([death])
  return send_choix()

## A fixer aussi

#import numba
#from numba import jit

#@numba.njit --> a tester en jit
def start_game(): #--> clique play
  G = game.copy()
  trois_choix = play_turn(G)
  return G, trois_choix

def player_play(G, ichoix): #--> clique choix
  trois_choix = play_turn(G, L_choix[ichoix])
  if len(trois_choix) < 2:
    return G, trois_choix
  else :
    return G, trois_choix #if len player_play  < 2 --> Game Over perso avec trois_choix
  
#ajouter une gestion de death



def show_death(G, trois_choix, L_death = L_death):

  if len(trois_choix) < 2:
    if trois_choix[0] > 0 :
      return L_death[trois_choix[0] - 1]
    
def conv_time(time):
  h = 20 + time//60
  m = time % 60
  if m < 10 :
    m = "0"+str(int(m))
  else :
    m = str(int(m))
  if h > 23 :
    h += -24
  if h < 10 :
    h = "0"+str(int(h))
  else :
    h = str(int(h))
  return(h+':'+m)

def bar_val(G, i, lims = lims):
  if i > len(lims[0]):
    return 0
  if G[i] <= lims[0][i - 1]:
    return 0.01
  if G[i]>=lims[1][i - 1]:
    return 0.99
  return G[i] / lims[1][i - 1]
