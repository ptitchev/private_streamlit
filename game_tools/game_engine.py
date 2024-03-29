import numpy as np
import json
import random
import pandas as pd
#import numba
#from numba import jit

#1: gestion de l'etat
with open("score.json", 'r') as f:
  dscore = json.load(f)

with open("ev.json", 'r') as f:
    data = json.load(f)
L_nom = np.array(data['index'])
L_params = np.array(data['columns'])
L_choix = np.array(data['data'])
L_choix[22][-1] = 4
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
           "Tout le monde avait trop faim ce soir, tu t'es fait dévoré par un autre qui avait plus faim que toi",
           "Faire la fête ou conduire, il faut choisir. Sur la route du retour, ta voiture a heurté un platane",
           "Le rythme de la musique était tellement entraînant que ton corps est resté possédé"]

L_musique = np.array(['Aucune','Rap','Rock','Techno','Commercial', 'House'])
d_musique = np.array([[0, 0, 0, 0, 0],
                      [-1, 1, 2, 0, -1],
                      [-1, 1, 1, -1, 1],
                      [0, 0, 3, -1, -1],
                      [0, 1, 0, 0, 0],
                      [1, -1, 1, 0, 0]])

#3 : Game et derrivées
game = np.zeros(19)
etat = np.array([0, 0, 80, 8, 0, 0, 5, 0])
depassements = np.zeros(7)
musique = np.zeros(1)
nb_tour = np.zeros(1)
score = np.zeros(1)
game[0:8] += game[0:8] + etat
game[8:15] += depassements
game[15] += musique
game[16] += nb_tour
game[17] += score

tres_der = np.array([np.zeros(8)] * 3)

data_choix = pd.DataFrame(L_choix, index = L_nom, columns = L_params)
data_lims = pd.DataFrame(lims.T, index = L_params[:-1], columns = ['-', '+'])
data_musique = pd.DataFrame(d_musique, index = L_musique, columns = L_params[2:-1])



def update_tres_der(t_der, choix):
  t_der[0] = t_der[1]
  t_der[1] = t_der[2]
  t_der[2] = choix

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
  dec = round((BPM)/20)
  dec = to_add * random.randint(0, dec)
  return BPM + dec

#@numba.njit
def update_etat(etat, choix):
  etat[1] = add_environ(etat[1], choix[0])
  etat[2] = add_BPM(etat[2], choix[1])
  for i in range(5):
    etat[i + 3] = add_environ(etat[i + 3], choix[i + 2])
  #return etat

def update_musique(G, musique = 0, lims = lims, d_musique = d_musique):
  mLims = lims[1][2:] + d_musique[musique]
  G[15] = musique
  return mLims

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
def check_etat(etat, depassements, limits):
  for i in range(7):
    if (i != 3) or (i != 4) :
      if lim_bas(etat, i+1, limits[0][i]):
        depassements[i] += -1
    if lim_haut(etat, i+1, limits[1][i]):
      depassements[i] += 1


#3: Gestion des condition de mort

#@numba.njit
def D_Zombie(depassements): #1
  if depassements[0] > 0:
    return True
  return False

def D_Indigestion(depassements): #2
  if depassements[5] > 1:
    return True
  return False

def D_Overdosed(depassements): #3
  if depassements[4] > 1:
    return True
  return False

def D_Exclue(depassements): #4
  if depassements[6] < -1:
    return True
  return False

def D_ethylique(depassements): #5
  if depassements[3] > 2:
    return True
  return False

def D_confiant(depassements): #6
  if (depassements[6] > 1) and (depassements[3] > 0) :
    return True
  return False

def D_allutination(depassements): #7
  if (depassements[4] > 0) and (depassements[5] < 0 ):
    return True
  return False

def D_cardiaque(depassements): #8
  if (depassements[1] > 1) or (depassements[1]< 0 ) or (depassements[2] > 1):
    return True
  return False

def D_affame(depassements): #9
  if depassements[5] < -1 :
    return True
  return False

#def D_Surplut() 3 vomis -> annulé

#def D_Volant() mort au volant #10

#def fou() danser au rythme endiablée avec drogue eleve #11
  
#@numba.njit
def check_dead(depassements):
  if D_Zombie(depassements):
    return 1
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

#Score
def calc_score(game, limits):
  if game[0] == -1 :
    w = 1000
  else :
    w = 0
  t = game[1]
  fact = np.prod((limits[1][3:] - np.abs((limits[1][3:] - 1) - game[4:8])) / limits[1][3:])
  s = int((w + (t * 2) - 5 * game[3]) * fact * 30)
  if s > 0 :
    game[-1] += s

def photo(game, t_der, limits):
  vect = np.sum(t_der, axis = 0)
  t = vect[0]
  fact = np.sum(np.abs(vect)) - t
  game[-1] += int(((t) * fact)/1000)

def manage_ev(game, choix, limits, t_der):

    if choix[-1] == 1:
      game[0] = -1

    elif choix[-1] == 2:
      if game[3] < limits[1][3]/2:
        game[0] = -1
      else : 
        game[0] = 0

    elif choix[-1] == 3:
      if  ((game[4] >= limits[1][4]/2) or (game[5] >= limits[1][5]/2)) :  
        game[0] = 1
      else :
        game[0] = -1 

    elif choix[-1] == -1:
      photo(game, t_der, limits)

    elif choix[-1] == 4 :
      if  ((game[4] > limits[1][4]-1) or (game[5] > limits[1][5]-1)) :  
         game[0] = 2
      else :
        game[0] = 0

#5: Jouer un tour

#@numba.njit
def play_turn(game, t_der, limits, choix = np.zeros(1), musique = 0):
  if len(choix) > 1:
    game[-2] += 1
    limits[1][2:] = update_musique(game, musique)
    manage_ev(game, choix, t_der, limits)
    update_tres_der(t_der, choix)

    if game[0] == 0 : #pas ev
      update_etat(game[0:8], choix)
      check_etat(game[0:8], game[8:15], limits)
      death = check_dead(game[8:15])
      if death > 0:
        game[0] = 1
        calc_score(game, limits)
        return np.array([death])

    elif game[0] == 1: #ev
      calc_score(game, limits)
      return np.array([10]) #a modifier en fonction (mort au volant)

    if game[0] == 2:
      game[0] = 1
      calc_score(game, limits)
      return np.array([11]) #a modifier en fonction (mort de danse --> bonus ?)

    if game[0] == -1:  #dors --> win / calcule score
      calc_score(game, limits)
      game[0] = 1
      return np.array([-1])
  

  if game[1] < 90 :
      return send_choix(19)
  elif game[1] < 180 :
      return send_choix(30)
  else :
      return send_choix()

## A fixer aussi

#import numba
#from numba import jit

#@numba.njit --> a tester en jit
def start_game(): #-->click play
  G = game.copy()
  t_der = tres_der.copy()
  limits = lims.copy()
  trois_choix = play_turn(G, t_der, limits)
  return G, t_der, trois_choix, limits

def player_play(G, t_der, limits, ichoix, musique): #--> clique choix
  trois_choix = play_turn(G, t_der, limits, L_choix[ichoix], musique)
  if len(trois_choix) < 2:
    return G, t_der, trois_choix, limits #--> game over
  else :
    return G, t_der, trois_choix, limits
#ajouter une gestion de death



def show_death(G, trois_choix, L_death = L_death):

  if len(trois_choix) < 2:
    if trois_choix[0] > 0 :
      return [0,L_death[trois_choix[0] - 1]]
    else :
      return [1, "Tu ressorts vivant de cette soirée d'anthologie"]
    
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



from io import BytesIO
import requests
from PIL import Image

L_image = []
url = 'https://raw.githubusercontent.com/ptitchev/private_streamlit/main/image 1024/'
for i in range(len(L_choix)):
  response = requests.get(url + str(i) + '.png')
  image = Image.open(BytesIO(response.content))
  L_image.append(image)