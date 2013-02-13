# this file GENERATES the avg/stddev needed for nhp


# new hero points
# idea:
# for each hero
#  analyze all matches with a player in them
#  look at all the players apart from that player (i.e., his peers)
#  come up with average and stddev  for each stat
# this makes the hero point windows unique to each player
# he is only compared to his peers, not to pro players

ANONYMOUS_ID = 4294967295


# points
#       -2o    -1o     x    +1o    +2o
#   -3      -1      0     1      3      5

# winning
# win < 20 = +5 pts
# win < 50 = +2 pts
# loss < 50 = +1 pts
# loss > 50 = +5 pts

# stats:
# kills, deaths, assists, gpm,
# last_hits, denies, xpm,
# hero_damage, tower_damage, hero_healing

# scores range from .. -3*10 +1 to 5*10+5
# that is, -29 to +55
# a solid score is an 12 ... 10*1 + 2

from models import *
import numpy
from db import session
import sys

import cPickle as pickle

import pprint
pp = pprint.PrettyPrinter(indent = 4)

name_id = {
 "alcaras": 32775483,
 "Rip" : 8899909,
 "Speed": 9541377,
 "Krygore" : 9929964,
 "Vorsh" : 703282,

 "m1gemini" : 8807692,
 "Wyv": 64684222,
 "Boozie" : 537293,

 "Don" : 33402007,
 "dgeis" : 100516439,
 

 "Anonymous" : ANONYMOUS_ID,
}

print "hello from the nhp"


# for each hero
#  analyze all matches with a player in them
#  look at all the players apart from that player (i.e., his peers)
#  come up with average and stddev  for each stat
# this makes the hero point windows unique to each player
# he is only compared to his peers, not to pro players

# step 1 -- we need a list of matches with the player in them
def obtain_matches_with_account_id(account_id):
    ids = []
    if account_id == ANONYMOUS_ID:
        l = session.query(Player.match_id).join(Player.match).filter_by(is_significant_p=True).all()
    else:
        l = session.query(Player.match_id).filter_by(account_id=account_id).join(Player.match).filter_by(is_significant_p=True).all()
    ids = [item for sublist in l for item in sublist]
    ids = list(set(ids))
    return ids

# analyze a set of player performances for a given hero
def analyze_player_performances(players):
    
    # we want avg and std dev for a variety of stats
    # stats comes from models

    data = {}
    avg = {}
    std = {}
    for s in stats:
        data[s] = []
        avg[s] = []
        std[s] = []

    for p in players:
        for s in stats:
            data[s] += [p.__dict__[s]]


            
    for s in stats:
        avg[s] = numpy.average(data[s])
        std[s] = numpy.std(data[s])


    return (avg, std)


pavg = {}
pstd = {}


for p, id in name_id.iteritems():
    # step 1 -- we need a list of matches with the player in them
    print "getting matches for ", p, "..."
    matches = obtain_matches_with_account_id(id)
    print len(matches), "matches found for ", p
    print "analyzing..."

    # now we need to go over all players in those matches
    # except our player
    # and do this by hero...

    heroes = session.query(Hero).all()

    havg = {}
    hstd = {}

    for hero in heroes:

#        print "Analyzing", hero.localized_name, "..."
        if id == ANONYMOUS_ID: # pull everything in for anon
            players = session.query(Player).filter(Player.hero == hero, Player.points > -100).join(Match).filter(Match.is_significant_p==True).all()
        else:
            players = session.query(Player).filter(Player.hero == hero, Player.account_id != id, Player.match_id.in_(matches), Player.points > -100).join(Match).filter(Match.is_significant_p==True).all()

        (havg[hero.id], hstd[hero.id]) = analyze_player_performances(players)

    pavg[id] = havg
    pstd[id] = hstd

hero_points = (pavg, pstd)

#pp.pprint(hero_points)


print "Pickling..."

jar = open('hero_points.pickle', 'wb')
pickle.dump(hero_points, jar)
jar.close()

print "Pickled."
        
        
        
        

    


