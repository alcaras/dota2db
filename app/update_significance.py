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
from constants import *

import sys

import pdb
import os

matches = session.query(Match).all()

flagged = 0

for i, m in enumerate(matches):
    if i % (len(matches)/20) == 0:
        print i+1, "/", len(matches)


    valid_modes = [0, 1, 2, 3, 4, 5, 12] # 0 is valid for legacy reasons
    if m.game_mode not in valid_modes:
        print "marking", m.id, "as insignificant: ",
        print "not a valid a game mode", m.game_mode,
        if m.game_mode in GAME_MODES:
            print GAME_MODES[m.game_mode]
        else:
            print "Unknown Game Mode"
        m.is_significant_p = False
        flagged += 1
        continue

        


    if m.human_players < 10:
        print "marking", m.id, "as insignificant: ",
        print "insufficient number of human players (", m.human_players, ")"
        m.is_significant_p = False
        flagged += 1
        continue


    if m.human_players < 10:
        print "marking", m.id, "as insignificant: ",
        print "insufficient number of human players (", m.human_players, ")"
        m.is_significant_p = False
        flagged += 1
        continue

    break_me = False

    for j, p in enumerate(m.players):
        if p.leaver_status >= 2: # 3s and 4s are not good
            print "marking", m.id, "as insignificant: ",
            print p.player_slot, "abandoned"
            m.is_significant_p = False
            break_me = True
            flagged += 1
            continue


    if break_me == True:
        continue

    m.is_significant_p = True
    

    
print flagged, "insignificant games"
session.commit()


