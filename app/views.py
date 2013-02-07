from app import app, db 

# idea: "team fight participation" stat
# sortable columns in match view (by team and overall)

import operator

from flask import render_template
from models import *

from constants import *

import pprint
pp = pprint.PrettyPrinter(indent = 4)


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page = 1):
    matches = Match.query.order_by(Match.starttime.desc()).paginate(page, MATCHES_PER_PAGE, False)
    
    # probably need to do this in two queries, for the sake of not hammering
    # the server with 20


    sorted_players = sorted(NAME_ID.iteritems(),
                            key=operator.itemgetter(0))
    sorted_players = sorted(sorted_players,
                            key = lambda s: s[0].lower())
    return render_template("index.html", matches = matches,
                           players = sorted_players)

@app.route('/match/<id>')
def match(id):
    return render_template("match.html", match_id = id)

@app.route('/player/<id>')
def player(id):
    return render_template("player.html", player_id = id)

