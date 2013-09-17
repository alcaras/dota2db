# update fantasy point range
# we do this once a day to make fantasy points scale between 0 and 100

from fantasy import calculate_fantasy_scores

from models import *
import numpy
from db import session
import sys

import cPickle as pickle

import pprint
pp = pprint.PrettyPrinter(indent = 4)


def obtain_all_matches():
    ids = []
    l = session.query(Player.match_id).join(Player.match).filter_by(is_significant_p=True).all()
    ids = [item for sublist in l for item in sublist]
    ids = list(set(ids))
    return ids

# analyze a set of player performances 
def analyze_player_performances(players):
    
    mina = {}
    maxa = {}

    first = True

    vectors = ["support", "carry", "solo"]
    for v in vectors:
        mina[v] = 0
        maxa[v] = 0

    for p in players:
        scores = calculate_fantasy_scores(p.__dict__)
        for v in vectors:
            if first == True:
                mina[v] = scores[v]
                maxa[v] = scores[v]
                first = False
            else:
                if scores[v] < mina[v]:
                    mina[v] = scores[v]
                if scores[v] > maxa[v]:
                    maxa[v] = scores[v]


    return (mina, maxa)


pavg = {}
pstd = {}


matches = obtain_all_matches()
print len(matches), "matches found"
print "analyzing..."

heroes = session.query(Hero).order_by(Hero.localized_name).all()

vectors = ["support", "carry", "solo"]

# global min and max; we can drill down by hero if we want
hmin = {}
hmax = {}

for v in vectors:
    hmin[v] = 0
    hmax[v] = 0

first = True
    
for i, hero in  enumerate(heroes):
    # just pull in everything
    print "Analyzing", hero.localized_name,
    print "(" + str(i+1) + " of", str(len(heroes)) + ")",
    players = session.query(Player).filter(Player.hero == hero).join(Match).filter(Match.is_significant_p==True).all()
    print "("+str(len(players)), "matches)..."
    
    (mina, maxa) = analyze_player_performances(players)

    for v in vectors:
        if first == True:
            hmin[v] = mina[v]
            hmax[v] = maxa[v]
            first = False
        else:
            if mina[v] < hmin[v]:
                hmin[v] = mina[v]
            if maxa[v] > hmax[v]:
                hmax[v] = maxa[v]


fpr_minmax = (hmin, hmax)

pp.pprint(fpr_minmax)


print "Pickling..."

jar = open('fpr_minmax.pickle', 'wb')
pickle.dump(fpr_minmax, jar)
jar.close()

print "Pickled."
        
        
        
        

    


