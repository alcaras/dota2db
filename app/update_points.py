# this file actually updates the points
from models import *
from db import session

from nhp import calculateHeroPoints

import sys

import pdb
import os

players = session.query(Player).all()

for i, p in enumerate(players):
    if i % (len(players)/20) == 0:
        print i+1, "/", len(players)
    p.points = calculateHeroPoints(p)

session.commit()
