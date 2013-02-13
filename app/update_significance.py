# https://dotabuff.com/players/32775483/matches?hero=&game_mode=&match_type=unreal

# var g_gamemodes = 
# {
# '1' : 'All Pick',
# '2' : "Captains Mode",
# '3' : 'Random Draft',
# '4' : 'Single Draft',
# '5' : 'All Random',
# '6' : '?? INTRO/DEATH ??',
# '7' : 'The Diretide',
# '8' : "Reverse Captains Mode",
# '9' : 'Greeviling',
# '10' : 'Tutorial',
# '11' : 'Mid Only',
# '12' : 'Least Played',
# '13' : 'New Player Pool'
# };

# valid modes = 1, 2, 3, 4, 5, 12

# look at leaver status for these matches, and figure out a trick to marking it insignifcant

# if human players < 10
# if the game mode is diretide or greeveling

# if a player has leaver_status >= 2
# and duration is less than X

# X 11:01
# 


# this file actually updates the points
from models import *
from db import session

from nhp import calculateHeroPoints

import sys

import pdb
import os

matches = session.query(Match).all()

for i, m in enumerate(matches):
    if i % (len(matches)/20) == 0:
        print i+1, "/", len(matches)


    print "marking", m.id, "as insignificant: ",
    print "insufficient number of human players (", m.human_players, ")"
    
    for j, p in m.players:
        continue
    

    

#session.commit()


