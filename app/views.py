from app import app, db 

# idea: "team fight participation" stat
# sortable columns in match view (by team and overall)

import string
import operator

from flask import render_template

from flask.ext.paginate import Pagination

from models import *

from constants import *

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
        helpers[m]["hero"] = {}
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
                    helpers[m]["kda"][p.player_slot] = str(round(float(p.kills + p.assists)/(p.deaths), 1))
                else:
                    helpers[m]["kda"][p.player_slot] = '&infin;'
                helpers[m]["lh/m"][p.player_slot] = str(round(float(p.last_hits)/float(match.duration/60),1))

                
                helpers[m]["hero"][p.player_slot] = "<img src=\"/static/img/" + string.replace(p.hero.name, "npc_dota_hero_", "") + "_sm.png\" alt=\"" + p.hero.localized_name + "\" title=\"" + p.hero.localized_name + "\" width=47 height=26 />"
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
    matches_pagination = Pagination(page=page, per_page = MATCHES_PER_PAGE, total=matches_query.count(), display_msg = display_msg)
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

@app.route('/match/<id>')
def match(id):
    match = Match.query.filter(Match.id == id).first()
    matches_query = [match]

    (matches, players_for_match, helpers) = matches_and_players(matches_query)
    
    return render_template("match.html", match = match, players_for_match=players_for_match, helpers=helpers)

@app.route('/player/<id>')
def player(id):
    return render_template("player.html", player_id = id)



