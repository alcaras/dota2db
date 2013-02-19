from app import app, db 

# idea: "team fight participation" stat
# sortable columns in match view (by team and overall)

import string
import operator


from flask import render_template
from flask import abort
from flask import request

from wilson import wilson
from confidence_interval import confidence_interval

# forking our own
from paginate import Pagination

from flask import g

from sqlalchemy.sql import func
from sqlalchemy import or_, and_

from models import *

from constants import *

import time
import datetime

import pprint
pp = pprint.PrettyPrinter(indent = 4)




def prepare_match_preview():
    fields = [ "player_slot",
               "player_name",
               "kda",
               "hero_points",
               "hero_icon",
               "kills",
               "deaths",
               "assists",
               "gold_per_min",
               "xp_per_min",
               "last_hits_per_min",
               "teamfight_participation",
               "items"
               ]
    return fields

def prepare_match_full():
    fields = [ "player_slot",
               "player_name",
               "kda",
               "hero_points",
               "hero_icon",
               "level",
               "kills",
               "deaths",
               "assists",
               "last_hits",
               "denies",
               "last_hits_per_min",
               "teamfight_participation",
               "gold_per_min",
               "xp_per_min",
               "hero_damage",
               "hero_healing",
               "tower_damage",
               "items"
               ]
    return fields




def matches_and_players(matches):

    match_ids = []
    for m in matches:
        match_ids += [m.id]


    players = Player.query.filter(Player.match_id.in_(match_ids)).all()

    players_for_match = {}
    for match in matches:
        m = match.id
        players_for_match[m] = []

        match.starttime += datetime.timedelta(hours=2)
        
        if match.game_mode in GAME_MODES:
            match.__setattr__("mode_name", GAME_MODES[match.game_mode])
        else:
            match.__setattr__("mode_name", "Game Mode " + str(match.game_mode))

        if match.cluster in CLUSTERS:
            match.__setattr__("cluster_name", CLUSTERS[match.cluster])
        else:
            match.__setattr__("cluster_name", "Cluster " + str(match.cluster))

        
        match.__setattr__("duration_pretty", str(datetime.timedelta(seconds=int(match.duration))))

        match.__setattr__("first_blood_time_pretty", str(datetime.timedelta(seconds=int(match.first_blood_time))))

        kills_radiant = 0
        kills_dire = 0

        for p in players:
            if p.match_id == m:
                if p.player_slot < 100:
                    kills_radiant += p.kills
                else:
                    kills_dire += p.kills

        for p in players:
            if p.match_id == m:

                players_for_match[m] += [p]
                if p.account_id in NAME_ID.values():
                    p.__setattr__("player_name", ID_NAME[p.account_id])            
                else:
                    p.__setattr__("player_name", "")

                if p.deaths > 0:
                    p.__setattr__("kda", (str(round(float(p.kills + p.assists) /
                                                                  (p.deaths), 1))))
                else:
                    p.__setattr__("kda", "&infin;")
                
                if match.duration/60 != 0:
                    p.__setattr__("lhpm", (str(round(float(p.last_hits) /
                                                                   float(match.duration/60),1))))
                else:
                    p.__setattr__("lhpm", "&infin;")

                tfp = float(p.kills + p.assists)
                if p.player_slot < 100:
                    if kills_radiant > 0:
                        tfp = float(tfp)/float(kills_radiant)
                else:
                    if kills_dire > 0:
                        tfp = float(tfp)/float(kills_dire)

                tfp = str(int(tfp * 100))
                        
                p.__setattr__("teamfight_participation", tfp)




    # okay the proper way to do this is to generate it here


    

    return (matches, players_for_match)
    

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page = 1):
    matches_query = Match.query.filter(Match.is_significant_p==True).order_by(Match.starttime.desc())
    display_msg = '''Matches <b>{start} - {end}</b> of 
<b>{total}</b>'''
    matches_pagination = Pagination(page=page, per_page = MATCHES_PER_PAGE,
                                    total=matches_query.count(), display_msg = display_msg)
    matches_query = matches_query.paginate(page, MATCHES_PER_PAGE, False)

    (matches, players_for_match) = matches_and_players(matches_query.items)


    sorted_players = sorted(NAME_ID.iteritems(),
                            key=operator.itemgetter(0))
    sorted_players = sorted(sorted_players,
                            key = lambda s: s[0].lower())

    start = 1 + (matches_pagination.page - 1) * matches_pagination.per_page
    end = start + matches_pagination.per_page - 1

    title = "Matches " + str(start) + " - " + str(end) + " of " + str(matches_pagination.total)
    
    return render_template("index.html", matches = matches_query,
                           pagination = matches_pagination,
                           players_for_match = players_for_match,
                           player_pages = sorted_players,
                           fields = prepare_match_preview(),
                           title = title)

@app.route('/match/<int:id>')
def match(id):
    match = Match.query.filter(Match.id == id).first()
    matches_query = [match]

    (matches, players_for_match) = matches_and_players(matches_query)

    fields = prepare_match_full()    
    if match.is_significant_p == False:
        fields += ["leaver_status"]

    title = "Match " + str(match.id)

    return render_template("match.html", match = match,
                           players_for_match=players_for_match,
                           fields = fields,
                           title = title)



@app.route('/player/<string:name>')
@app.route('/player/<string:name>/page/<int:page>')
def player(name, page = 1):

    if str(name) in NAME_ID.keys():
        player_name = name
        player_id = NAME_ID[str(name)]
    else:
        abort(404)


    matches_query = Match.query.join(Player).\
        filter(Player.account_id==player_id,
               Match.is_significant_p==True).\
        order_by(Match.starttime.desc())
    display_msg = '''Matches <b>{start} - {end}</b> of <b>{total}</b>'''
    matches_pagination = Pagination(per_page = MATCHES_PER_PAGE,
                                    total=matches_query.count(),
                                    display_msg = display_msg,
                                    page = page)
    matches_query = matches_query.paginate(page, MATCHES_PER_PAGE, False)

    (matches, players_for_match) = matches_and_players(matches_query.items)


    title = player_name

    return render_template("player.html", matches = matches_query,
                           pagination = matches_pagination,
                           players_for_match = players_for_match,
                           player_name = player_name,
                           fields = prepare_match_preview(),
                           title = title)








@app.route('/player/<string:name>/heroes')
def player_heroes(name):

    if str(name) in NAME_ID.keys():
        player_name = name
        player_id = NAME_ID[str(name)]
    else:
        abort(404)

    stmt = db.session.query(Hero,
                            func.count(Player.account_id).label("played"),
                            func.sum(Player.win > 0, type_=Integer).label("wins"),
                            func.sum(Player.kills).label("kills_sum"),
                            func.sum(Player.deaths).label("deaths_sum"),
                            func.sum(Player.assists).label("assists_sum"),
                            func.avg(Player.points).label("points_avg")).\
                            outerjoin(Player).\
                            outerjoin(Player.match).\
                            filter(Match.is_significant_p == True,
                                   Player.account_id == player_id).\
                                   group_by(Hero.id).\
                                   order_by(Hero.localized_name).\
                                   subquery()

    heroes_query = db.session.query(Hero, stmt.c.played,
                                    stmt.c.wins,
                                    stmt.c.kills_sum,
                                    stmt.c.deaths_sum,
                                    stmt.c.assists_sum,
                                    stmt.c.points_avg).outerjoin(stmt, Hero.id == stmt.c.id).\
                                    order_by(Hero.localized_name).all()

    # we also need to pull the entire points distribution...
    heroes_points = db.session.query(Player.points,
                                     Hero).\
                                     join(Player.match).\
                                     join(Hero).\
                                     filter(Match.is_significant_p==True,
                                            Player.account_id==player_id).\
                                            all()

    # hero point distributions
    hpd = {}
       
    for hp in heroes_points:
        if hp.Hero.id not in hpd:
            hpd[hp.Hero.id] = []
        hpd[hp.Hero.id] += [hp.points]


    for h in heroes_query:
        if h.Hero.id not in hpd:
            hpd[h.Hero.id] = []

        if h.wins is None:
            h.wins = 0

        if h.played is None:
            h.played = 0

        if h.played > 0:
            win_pct = (round(float(h.wins)/h.played*100,1))
        else:
            win_pct = (round(float(0.0)*100,1))
        
        if h.points_avg is not None:
            h.points_avg = round(h.points_avg, 1)
        else:
            h.points_avg = 0.0

        kda = "&infin;"
        if h.deaths_sum > 0:
            kda = str(round(float(h.kills_sum + h.assists_sum) / (h.deaths_sum), 1))
        if h.played == 0:
            kda = "0.0"




        # arbitrary scaling factor for prettier numbers
        win_wilson = round(wilson(h.played, h.wins)*100,1)

        ci = confidence_interval(hpd[h.Hero.id])

        points_lb_ci = 0.0  

        if ci != None:
            points_lb_ci = round(ci[0],1)
        
        if points_lb_ci < 0:
            points_lb_ci = 0.0

        h.__setattr__("win_pct", win_pct)            
        h.__setattr__("kda", kda)
        h.__setattr__("win_wilson", win_wilson)
        h.__setattr__("points_lb_ci", points_lb_ci)


    title = player_name + "'s Heroes"

    return render_template("player-heroes.html",
                           heroes = heroes_query,
                           player_name = player_name,
                           title = title)




