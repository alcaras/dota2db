# this file actually updates the points
from models import *
from db import session

from nhp import calculateHeroPoints

import sys

import pdb
import os

players = session.query(Player).all()
#players = session.query(Player).filter(Player.account_id == 32775483).order_by(Player.match_id.desc()).all()

for i, p in enumerate(players):
    if i % (len(players)/20) == 0:
        print i+1, "/", len(players)

    if p.match is None:
        continue

    p.points = calculateHeroPoints(p)

# old code to update win/loss
#     # 0, 1, 2, 3, 4 are Radiant
#     # 128, 129, 130, 131, 132 are Dire
#     if p.player_slot < 128: # Radiant
#       if p.match.radiant_win == True:
#         p.win = True
#       else:
#         p.win = False
#     else: # dire
#       if p.match.radiant_win == False:
#         p.win = True
#       else:
#         p.win = False

session.commit()
