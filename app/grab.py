import traceback
from api import *

from constants import *

import json
import sqlalchemy
from models import Match, Player
from db import session
import pprint
pp = pprint.PrettyPrinter(indent = 4)
import pdb
import sys

from nhp import calculateHeroPoints

print "hello from the webapi grab"

name_id = NAME_ID

# two ways of operatinig
# 1. full grab -- grab everything, overwrite matches with the same id
#    (e.g. if adding someone new)
# 2. refresh -- grab just matches within the last X (date_min)
#    (don't overwrite matches)

refreshOnly = True # usually should be true, unless you're adding someone new

fullCrawlFor = "" # set this to an id to full crawl
enableFullCrawl = False # set this to true for a full crawl (for a particular person)

import datetime
import time

# return a list of match ids, given a player id
# note: goes all the way back

def grab_match_ids(**kwargs):
  ids = []
  
  start_at_match_id = None
  date_max = None

  
 
  while True:
      rout = get_match_history(start_at_match_id = start_at_match_id,
                               date_max = date_max,
                               **kwargs)
      if rout == None:
        print "got None, skipping match history", start_at_match_id, date_max
        continue

      matches = rout.json()
      
      if matches["result"]["status"] != 1:
        print "Status Code ", matches["result"]["status"],
        if "statusDetail" in matches["result"]:
          print matches["result"]["statusDetail"]
          return ids

      if matches["result"]["num_results"] == 0:
          break
      print "got",matches["result"]["num_results"],"matches starting at", start_at_match_id,
      print "date_max", date_max,
      print "\tat least",matches["result"]["results_remaining"],"remaining..."
      for a in matches["result"]["matches"]:
          ids += [a["match_id"]]
          start_at_match_id = a["match_id"] -1
          date_max = a["start_time"] - 1


  return ids    
    


def grab_match(id):
  # check if the id already exists
  if session.query(Match).filter(Match.id == id).first() is not None:
    print " Match already parsed."
    if enableFullCrawl == False:
      return -1 # already parsed
    else:
      print " Dropping this match"
      # drop this match and associated players
      session.delete(session.query(Match).filter(Match.id == id).first())
      players_in_this_match = session.query(Player).filter(Player.match_id == id).all()
      for p in players_in_this_match:
        session.delete(p)
      session.commit()
      print " Match dropped."


  
  print "Parsing new match " + str(id)

  abandons = 0
  
  req = get_match_details(id)
  if req == None:
    print "Got None, skipping...",id
    return -1
  json_req = req.json()

  try:
    details =   req.json()["result"]
  except KeyError:
    print "Weird results, skipping..."
    pp.pprint(json_req)
    return -1

  try:
  

    match = {}

    match["id"] = details["match_id"]

    match["barracks_status_dire"] = details["barracks_status_dire"]
    match["barracks_status_radiant"] = details["barracks_status_radiant"]
    match["cluster"] = details["cluster"]
    match["duration"] = details["duration"]
    match["first_blood_time"] = details["first_blood_time"]
    match["game_mode"] = details["game_mode"]
    match["human_players"] = details["human_players"]
    match["leagueid"] = details["leagueid"]
    match["negative_votes"] = details["negative_votes"]
    match["positive_votes"] = details["positive_votes"]
    match["radiant_win"] = details["radiant_win"]
    match["season"] = details["season"]
    match["starttime"] = datetime.datetime.fromtimestamp(details["start_time"])
    match["tower_status_dire"] = details["tower_status_dire"]
    match["tower_status_radiant"] = details["tower_status_radiant"]
    
  except KeyError, e:
    print  datetime.datetime.now(), "Exception:", e, sys.exc_info()[0]
    print '-'*60
    traceback.print_exc(file=sys.stdout)
    print '-'*60
    pp.pprint(details)

  # is_significant_p needs to be set based on players
  # for now -- since we don't know how leaver status works, we just use
  # true
  match["is_significant_p"] = True
  
  # create the game
  new_match = Match(match["id"], match["barracks_status_dire"],
                   match["barracks_status_radiant"], match["cluster"],
                   match["duration"], match["first_blood_time"],
                   match["game_mode"], match["human_players"],
                   match["leagueid"], match["negative_votes"],
                   match["positive_votes"], match["radiant_win"],
                   match["season"], match["starttime"],
                   match["tower_status_dire"], match["tower_status_radiant"],
                   match["is_significant_p"])

  new_match.players = []
      
  players = details["players"]

  for p in players:
    pl = {}


    pl["win"] = False

    pl["player_slot"] = p["player_slot"]

    # 0, 1, 2, 3, 4 are Radiant
    # 128, 129, 130, 131, 132 are Dire
    if p["player_slot"] < 128: # Radiant
      if match["radiant_win"] == True:
        pl["win"] = True
      else:
        pl["win"] = False
    else: # dire
      if match["radiant_win"] == False:
        pl["win"] = True
      else:
        pl["win"] = False



    # player id
    pl["account_id"]= p["account_id"]

    # hero_id
    pl["hero_id"] = p["hero_id"]
    
    # level
    pl["level"] = p["level"]
    
    # kills
    pl["kills"] = p["kills"]

    # deaths
    pl["deaths"] = p["deaths"]
    
    # assists
    pl["assists"] = p["assists"]

    # gold
    pl["gold"] = p["gold"]

    # last hits
    pl["last_hits"] = p["last_hits"]

    # denies
    pl["denies"] = p["denies"]
    
    # xpm
    pl["xp_per_min"] = p["xp_per_min"]

    # gpm
    pl["gold_per_min"] = p["gold_per_min"]
    
    # items
    pl["item_0"] = p["item_0"]
    pl["item_1"] = p["item_1"]
    pl["item_2"] = p["item_2"]
    pl["item_3"] = p["item_3"]
    pl["item_4"] = p["item_4"]
    pl["item_5"] = p["item_5"]
    



    pl["gold"] = p["gold"]
    pl["gold_spent"] = p["gold_spent"]
    pl["hero_damage"] = p["hero_damage"]
    pl["hero_healing"] = p["hero_healing"]
    pl["tower_damage"] = p["tower_damage"]
    
    # 0 = okay, 1 = left after safe, 2 = abandon, 3 = ?, 4 = ?
    pl["leaver_status"] = p["leaver_status"]
    if pl["leaver_status"] >= 2:
      abandons += 1
    

    # players = [player, hero, level, k, d, a, lh, dn, xpm, gpm, [items]]
    new_player = Player(pl["account_id"], pl["assists"], pl["deaths"],
                        pl["denies"], pl["gold"], pl["gold_per_min"],
                        pl["gold_spent"], pl["hero_damage"], pl["hero_healing"],
                        pl["hero_id"], pl["item_0"], pl["item_1"],
                        pl["item_2"], pl["item_3"], pl["item_4"],
                        pl["item_5"], pl["kills"], pl["last_hits"],
                        pl["leaver_status"], pl["level"],
                        pl["player_slot"], pl["tower_damage"],
                        pl["xp_per_min"], pl["win"])


    new_player.points = calculateHeroPoints(new_player, duration=match["duration"])

  
    
    new_match.players.extend([new_player])

  
  new_match.is_significant_p = True

  valid_modes = [0, 1, 2, 3, 4, 5, 12] # 0 is valid for legacy reasons
  if new_match.game_mode not in valid_modes:
    new_match.is_significant_p = False

  if new_match.human_players < 10:
    new_match.is_significant_p = False

  if abandons > 0:
    new_match.is_significant_p = False

    
  session.add(new_match)
  session.commit()
  return 1 # all good


date_min = None

if refreshOnly == True:
  date_min = int(time.mktime((datetime.datetime.now() - datetime.timedelta(hours=48)).timetuple()))
  print "only refreshing back to", datetime.datetime.fromtimestamp(date_min)

rid = []

if enableFullCrawl == True:
  name_id = { fullCrawlFor : name_id[fullCrawlFor] }

for k,v in name_id.iteritems():
  print "Grabbing matches for", k
  new_matches = grab_match_ids(account_id = v, date_min = date_min)
  print len(new_matches), "matches found for", k
  rid += new_matches

rid = list(set(rid))

for i, id in enumerate(rid):
  print "Grabbing match ", i, "of", len(rid)-1, ":\t", id, "..."
  grab_match(id)


