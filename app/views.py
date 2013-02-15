from app import app, db 

# idea: "team fight participation" stat
# sortable columns in match view (by team and overall)

import string
import operator


from flask import render_template
from flask import abort
from flask import request


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


def matches_and_players(matches):

    match_ids = []
    for m in matches:
        match_ids += [m.id]


    players = Player.query.filter(Player.match_id.in_(match_ids)).all()

    helpers = {}

    players_for_match = {}
    for match in matches:
        m = match.id
        players_for_match[m] = []
        helpers[m] = {}
        helpers[m]["p"] = {}
        helpers[m]["kda"] = {}
        helpers[m]["lh/m"] = {}

        if match.game_mode in GAME_MODES:
            helpers[m]["mode"] = GAME_MODES[match.game_mode]
        else:
            helpers[m]["mode"] = "Game Mode " + str(match.game_mode)

        if match.cluster in CLUSTERS:
            helpers[m]["cluster"] = CLUSTERS[match.cluster]
        else:
            helpers[m]["cluster"] = "Cluster " + str(match.cluster)

        helpers[m]["duration"] = str(datetime.timedelta(seconds=int(match.duration)))

        for p in players:
            if p.match_id == m:
                players_for_match[m] += [p]
                if p.account_id in NAME_ID.values():
                    helpers[m]["p"][p.player_slot] = ID_NAME[p.account_id]
                else:
                    helpers[m]["p"][p.player_slot] = ''
                if p.deaths > 0:
                    helpers[m]["kda"][p.player_slot] = (str(round(float(p.kills + p.assists) /
                                                                  (p.deaths), 1)))
                else:
                    helpers[m]["kda"][p.player_slot] = '&infin;'
                
                if match.duration/60 != 0:
                    helpers[m]["lh/m"][p.player_slot] = (str(round(float(p.last_hits) /
                                                                   float(match.duration/60),1)))
                else:
                     helpers[m]["lh/m"][p.player_slot] = '&infin;'

                # 47x26                





                

    # okay the proper way to do this is to generate it here


    

    return (matches, players_for_match, helpers)
    


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page = 1):
    matches_query = Match.query.order_by(Match.starttime.desc())
    display_msg = '''Matches <b>{start} - {end}</b> of 
<b>{total}</b>'''
    matches_pagination = Pagination(page=page, per_page = MATCHES_PER_PAGE,
                                    total=matches_query.count(), display_msg = display_msg)
    matches_query = matches_query.paginate(page, MATCHES_PER_PAGE, False)

    (matches, players_for_match, helpers) = matches_and_players(matches_query.items)


    sorted_players = sorted(NAME_ID.iteritems(),
                            key=operator.itemgetter(0))
    sorted_players = sorted(sorted_players,
                            key = lambda s: s[0].lower())
    
    return render_template("index.html", matches = matches_query,
                           pagination = matches_pagination,
                           players_for_match = players_for_match,
                           helpers = helpers,
                           player_pages = sorted_players)

@app.route('/match/<int:id>')
def match(id):
    match = Match.query.filter(Match.id == id).first()
    matches_query = [match]

    (matches, players_for_match, helpers) = matches_and_players(matches_query)
    
    return render_template("match.html", match = match,
                           players_for_match=players_for_match, helpers=helpers)

@app.route('/player/<string:name>')
@app.route('/player/<string:name>/page/<int:page>')
def player(name, page = 1):

    if str(name) in NAME_ID.keys():
        player_name = name
        player_id = NAME_ID[str(name)]
    else:
        abort(404)


    matches_query = Match.query.join(Player).\
        filter(Player.account_id==player_id).\
        order_by(Match.starttime.desc())
    display_msg = '''Matches <b>{start} - {end}</b> of <b>{total}</b>'''
    matches_pagination = Pagination(per_page = MATCHES_PER_PAGE,
                                    total=matches_query.count(),
                                    display_msg = display_msg,
                                    page = page)
    matches_query = matches_query.paginate(page, MATCHES_PER_PAGE, False)

    (matches, players_for_match, helpers) = matches_and_players(matches_query.items)




    return render_template("player.html", matches = matches_query,
                           pagination = matches_pagination,
                           players_for_match = players_for_match,
                           helpers = helpers,
                           player_name = player_name)





@app.route('/player/<string:name>')
@app.route('/player/<string:name>/page/<int:page>')
def player(name, page = 1):

    if str(name) in NAME_ID.keys():
        player_name = name
        player_id = NAME_ID[str(name)]
    else:
        abort(404)


    matches_query = Match.query.join(Player).\
        filter(Player.account_id==player_id).\
        order_by(Match.starttime.desc())
    display_msg = '''Matches <b>{start} - {end}</b> of <b>{total}</b>'''
    matches_pagination = Pagination(per_page = MATCHES_PER_PAGE,
                                    total=matches_query.count(),
                                    display_msg = display_msg,
                                    page = page)
    matches_query = matches_query.paginate(page, MATCHES_PER_PAGE, False)

    (matches, players_for_match, helpers) = matches_and_players(matches_query.items)




    return render_template("player.html", matches = matches_query,
                           pagination = matches_pagination,
                           players_for_match = players_for_match,
                           helpers = helpers,
                           player_name = player_name)





@app.route('/player/<string:name>/heroes')
def player_heroes(name):

    if str(name) in NAME_ID.keys():
        player_name = name
        player_id = NAME_ID[str(name)]
    else:
        abort(404)

    heroes_query = db.session.query(Hero,
                                    func.count(Player.account_id).label("played"),
                                    func.sum(Player.win > 0, type_=Integer).label("wins"),
                                    func.sum(Player.kills).label("kills_sum"),
                                    func.sum(Player.deaths).label("deaths_sum"),
                                    func.sum(Player.assists).label("assists_sum"),
                                    func.avg(Player.points).label("points_avg"),).\
                                    outerjoin(Player).\
                                    outerjoin(Player.match).\
                                    filter(or_(and_(Player.account_id == player_id,
                                                    Match.is_significant_p == True),
                                               and_(Player.account_id == None,
                                                    Match.is_significant_p == None))).\
                                    group_by(Hero.id).\
                                    order_by(Hero.localized_name).\
                                    all()

    for h in heroes_query:
        if h.wins is None:
            h.wins = 0

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

        h.__setattr__("win_pct", win_pct)
            
        h.__setattr__("kda", kda)


    
    return render_template("player-heroes.html",
                           heroes = heroes_query,
                           player_name = player_name)




