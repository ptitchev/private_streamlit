import numpy as np
import random
import time
#import numba
#from numba import jit

import game_engine as GE
from ref import game, L_choix

#@numba.njit --> a tester en jit
def start_game(): #--> clique play
  G = game.copy()
  trois_choix = GE.play_turn(G)
  return G, trois_choix

def player_play(G, ichoix): #--> clique choix
  trois_choix = GE.play_turn(G, L_choix[ichoix])
  if len(trois_choix) < 2:
    return trois_choix
  else :
    return G, trois_choix #if len player_play  < 2 --> Game Over perso avec trois_choix