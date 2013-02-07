# this file CALCULATES new hero points

# ideas -- stats by roles
# if a hero is a carry, last_hits counts
# k d a gpm counts for all
# hero_damage counts for non-supports
# tower_damage counts for pushers
# hero_healing counts for supports
import pdb


ANONYMOUS_ID = "4294967295"

# points
#       -2o    -1o     x    +1o    +2o
#   -3      -1      0     1      3      5

# winning
# win < 20 = +5 pts
# win > 20 = +2 pts
# loss < 50 = +1 pts
# loss > 50 = +5 pts

# stats:
# kills, deaths, assists, gpm,
# last_hits, denies, xpm,
# hero_damage, tower_damage, hero_healing

# scores range from .. -3*10 +1 to 5*10+5
# that is, -29 to +55
# a solid score is an 12 ... 10*1 + 2

# scores range from -3*28+1 to 5*28+5
# that is, -53 to 185
# we can shift and scale

stat_weights = {"kills" : 5,
                "deaths" : 5,
                "assists" : 5,
                "gold_per_min" : 3,
                "xp_per_min" : 3,
                "last_hits" : 2,
                "denies" : 2,
                "hero_damage" : 1,
                "tower_damage" : 1,
                "hero_healing" : 1, }

from models import *
from db import session

ANONYMOUS_ID = 4294967295

import pprint
pp = pprint.PrettyPrinter(indent = 4)
from new_hero_points import hero_avg, hero_std
import math
import sys

# calculate hero points for a player
def calculateHeroPoints(p):
    
    a = p.account_id
    if a not in hero_avg:
        a = ANONYMOUS_ID # use anonymous for people we don't know
        
    h = p.hero_id

    if p.match_id == None: # why are there players with empty matches?
        # if p.account_id == ANONYMOUS_ID:
        #     print ".. anon null match_id"
        # elif a == ANONYMOUS_ID:
        #     print ".. pseudo anon null match_id", p.account_id
        # else:
        #     print "!! non anon null match_id", p.account_id
        return -100
    
    if math.isnan(float(hero_avg[a][h][stats[0]])):
        return -100

    score = 0

# points
#       -2o    -1o     x    +1o    +2o        standard deviations from average
#   -3      -1      0     1      3      5     points for falling into a range

    for s in stats:
        k = p.__dict__[s]

        bonus = 0

        if k >= float(hero_avg[a][h][s] + 2*hero_std[a][h][s]):
            bonus = 5
        elif k >= float(hero_avg[a][h][s] + 1*hero_std[a][h][s]):
            bonus = 3
        elif k >= float(hero_avg[a][h][s] + 0*hero_std[a][h][s]):
            bonus = 1
        elif k >= float(hero_avg[a][h][s] + -1*hero_std[a][h][s]):
            bonus  =0
        elif k >= float(hero_avg[a][h][s] + -2*hero_std[a][h][s]):
            bonus = -1
        else:
            bonus = -3

        score += stat_weights[s] * bonus

        dis = p.match.duration
        if dis <= (20*60) and (p.win==1):
            score += 5  # stomp bonus
        if dis > (20*60) and (p.win==1):
            score += 3 # a standard win
        if dis < (50*60) and (p.win==0):
            score += 1 # consolation prize
        if dis >= (50*60) and (p.win==0):
            score += 2 # bonus for holding out so long

    # scale
    scaled_score = (score + 3*28-1) # add base
    scaled_score = float(scaled_score) / 228.0 * 100
    scaled_score = round(scaled_score, 0)
    
    

    return scaled_score
