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

# we're going to look at a different set of stats
# kills+assists
# deaths
# gpm

# we can shift and scale
# our lowest score is -3*5 (-15)
# our high score is 5*5 (25)

stat_weights = {"kills" : 1,
                "deaths" : 1,
                "assists" : 1,
                "gold_per_min" : 1,
                "xp_per_min" : 1,
                "tower_damage": 1,
                "hero_damage": 1,
                "hero_healing": 1,
                "last_hits" : 1,
                "denies" : 1}

from models import *
from db import session

ANONYMOUS_ID = 4294967295

import pprint
pp = pprint.PrettyPrinter(indent = 4)
from new_hero_points import hero_avg, hero_std
import math
import sys

# calculate hero points for a player
def calculateHeroPoints(p, duration=None):
    
#    a = p.account_id
#    if a not in hero_avg:
    a = ANONYMOUS_ID # use anonymous for people we don't know
        
    h = p.hero_id

    if duration == None and p.match_id == None: # why are there players with empty matches?
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

 #   print 
#    print p.hero

# points
#       -2o    -1o     x    +1o    +2o        standard deviations from average
#   -3      -1      0     1      3      5     points for falling into a range


    for s in stats:
        k = p.__dict__[s]

        if duration == None:
            dis = p.match.duration
        else:
            dis = duration

        dim = int(dis/60)

        
        old_k = k
        if s in stats_to_per_min: # we need to divide by duration
            if dim == 0:
                k = 0 # can't divide by 0
            else:
                k = float(k) / float(dim)


        bonus = 0

        if s != "deaths":
            
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

        else: # deaths is inverted, as less is more

            if k <= float(hero_avg[a][h][s] + -2*hero_std[a][h][s]):
                bonus = 5
            elif k <= float(hero_avg[a][h][s] + -1*hero_std[a][h][s]):
                bonus = 3
            elif k <= float(hero_avg[a][h][s] + 0*hero_std[a][h][s]):
                bonus = 1
            elif k <= float(hero_avg[a][h][s] + 1*hero_std[a][h][s]):
                bonus  =0
            elif k <= float(hero_avg[a][h][s] + 2*hero_std[a][h][s]):
                bonus = -1
            else:
                bonus = -3

#        print s, old_k, k, "a", hero_avg[a][h][s], hero_std[a][h][s], bonus

        score += stat_weights[s] * bonus

#         if dis <= (20*60) and (p.win==1):
#             score += 5  # stomp bonus
#         if dis > (20*60) and (p.win==1):
#             score += 3 # a standard win
#         if dis < (50*60) and (p.win==0):
#             score += 1 # consolation prize
#         if dis >= (50*60) and (p.win==0):
#             score += 2 # bonus for holding out so long

    # scale
    

#    print score
            

    lowest_score = 0
    for s in stats:
        lowest_score += abs(stat_weights[s]) * -3

#    print lowest_score

    highest_score = 0
    for s in stats:
        highest_score += abs(stat_weights[s]) * 5

#    print highest_score

    range = highest_score - lowest_score + 1

#    print range

    scaled_score = (score - (lowest_score)) # subtract the lowest possible score
    # divide by our score range
    scaled_score = float(scaled_score) / range * 100 # range over 0-100
    scaled_score = round(scaled_score, 0)

#    print scaled_score
    
    

    return scaled_score
