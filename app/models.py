from flask import render_template

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, BigInteger, Boolean, Integer, String, DateTime, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

import string
import pdb

try:
    from app import db
    Base = db.Model           # for use with flask
except ImportError:
    Base = declarative_base() # for use without flask (e.g. cronjobs)

#Base = declarative_base()

all_stats = ["assists", "kills", "deaths",
         "gold_per_min", "hero_healing",
         "xp_per_min",
         "last_hits", "denies",
         "tower_damage", "hero_damage", 
]
 
# stats we care about
stats = ["assists", "kills", "deaths",
         "gold_per_min", "xp_per_min",
]

class Match(Base):
    __tablename__ = 'matches'
    id = Column(BigInteger, primary_key=True)
    
    barracks_status_dire = Column(Integer)
    barracks_status_radiant = Column(Integer)
    cluster = Column(Integer)
    duration = Column(Integer)
    first_blood_time = Column(Integer)
    game_mode = Column(Integer)
    human_players = Column(Integer)
    leagueid = Column(Integer)
    negative_votes = Column(Integer)
    positive_votes = Column(Integer)
    radiant_win = Column(Boolean)
    season = Column(Integer)
    starttime = Column(DateTime)
    tower_status_dire = Column(Integer)
    tower_status_radiant = Column(Integer)

    is_significant_p = Column(Boolean)

    def __init__(self, id, barracks_status_dire, barracks_status_radiant,
                 cluster, duration, first_blood_time, game_mode, human_players,
                 leagueid, negative_votes, positive_votes, radiant_win,
                 season, starttime, tower_status_dire, tower_status_radiant,
                 is_significant_p):
        self.id = id
        self.barracks_status_dire = barracks_status_dire
        self.barracks_status_radiant = barracks_status_radiant
        self.cluster = cluster
        self.duration = duration
        self.first_blood_time = first_blood_time
        self.game_mode = game_mode
        self.human_players = human_players
        self.leagueid = leagueid
        self.negative_votes = negative_votes
        self.positive_votes = positive_votes
        self.radiant_win = radiant_win
        self.season = season
        self.starttime = starttime
        self.tower_status_dire = tower_status_dire
        self.tower_status_radiant = tower_status_radiant
        self.is_significant = is_significant_p
        
    def radiant_tower(self, which):
        if (self.tower_status_radiant & which) == which:
            return "badge-success"
        else:
            return ""

    def radiant_barracks(self, which):
        if (self.barracks_status_radiant & which) == which:
            return "badge-success"
        else:
            return ""

    def dire_tower(self, which):
        if (self.tower_status_dire & which) == which:
            return "badge-important"
        else:
            return ""

    def dire_barracks(self, which):
        if (self.barracks_status_dire & which) == which:
            return "badge-important"
        else:
            return ""




    def buildings(self):
        return render_template("building-display.html",
                               match = self)

        
    def __repr__(self):
        return "<Match('%s')>" % (self.id)

class Player(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    match = relationship("Match", backref=backref('players', order_by=id))

    account_id = Column(BigInteger)
    assists = Column(Integer)
    deaths = Column(Integer)
    denies = Column(Integer)
    gold = Column(Integer)
    gold_per_min = Column(Integer)
    gold_spent = Column(Integer)
    hero_damage = Column(Integer)
    hero_healing = Column(Integer)
    hero_id = Column(Integer, ForeignKey('heroes.id'))
    hero = relationship("Hero")
    item_0 = Column(Integer, ForeignKey('items.id'))
    item0 = relationship("Item", primaryjoin="Player.item_0 == Item.id")
    item_1 = Column(Integer, ForeignKey('items.id'))
    item1 = relationship("Item", primaryjoin="Player.item_1 == Item.id")
    item_2 = Column(Integer, ForeignKey('items.id'))
    item2 = relationship("Item", primaryjoin="Player.item_2 == Item.id")
    item_3 = Column(Integer, ForeignKey('items.id'))
    item3 = relationship("Item", primaryjoin="Player.item_3 == Item.id")
    item_4 = Column(Integer, ForeignKey('items.id'))
    item4 = relationship("Item", primaryjoin="Player.item_4 == Item.id")
    item_5 = Column(Integer, ForeignKey('items.id'))
    item5 = relationship("Item", primaryjoin="Player.item_5 == Item.id")
    kills = Column(Integer)
    last_hits = Column(Integer)
    leaver_status = Column(Integer)
    level = Column(Integer)
    player_slot = Column(Integer)
    tower_damage = Column(Integer)
    xp_per_min = Column(Integer)
    
    win = Column(Boolean)
    points = Column(Integer)

    def __init__(self, account_id, assists, deaths, denies, gold, gold_per_min, gold_spent, hero_damage, hero_healing, hero_id, item_0, item_1, item_2, item_3, item_4, item_5, kills, last_hits, leaver_status, level, player_slot, tower_damage, xp_per_min, win):

        self.account_id = account_id
        self.assists = assists 
        self.deaths = deaths
        self.denies = denies 
        self.gold = gold 
        self.gold_per_min = gold_per_min 
        self.gold_spent = gold_spent 
        self.hero_damage = hero_damage 
        self.hero_healing = hero_healing 
        self.hero_id = hero_id 
        self.item_0 = item_0 
        self.item_1 = item_1 
        self.item_2 = item_2 
        self.item_3 = item_3 
        self.item_4 = item_4 
        self.item_5 = item_5 
        self.kills = kills 
        self.last_hits = last_hits 
        self.leaver_status = leaver_status 
        self.level = level 
        self.player_slot = player_slot 
        self.tower_damage = tower_damage 
        self.xp_per_min = xp_per_min 
    
        self.win = win
        self.points = 0

    def __repr__(self):
        return "<Player('%s', '%s', '%s')>" % (self.match_id, self.account_id, self.hero)

class Hero(Base):
    __tablename__ = 'heroes'
    id = Column(Integer, primary_key=True)
    localized_name = Column(String)
    name = Column(String)
    def __init__(self, id, localized_name, name):
        self.id = id
        self.localized_name = localized_name
        self.name = name
    def __repr__(self):
        return "<Hero('%s', '%s', '%s')>" % (self.id, self.localized_name, self.name)
    def img_inline(self):
        short_name = string.replace(self.name, "npc_dota_hero_", "")
        return render_template('inline-image.html', hero=self,
                               short_name = short_name)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    localized_name = Column(String)
    name = Column(String)
    def __init__(self, id, localized_name, name):
        self.id = id
        self.localized_name = localized_name
        self.name = name
    def __repr__(self):
        return "<Item('%s', '%s', '%s')>" % (self.id, self.localized_name, self.name)

