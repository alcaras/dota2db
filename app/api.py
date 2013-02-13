# todo:
# - need to figure out what time zone we're getting responses in
# - and whether or not it is dependent on what time zone we are in
"""
Tools for accessing the Dota 2 match history web API
"""
import traceback
import datetime
import sys
import time
SLEEP_DELAY = 1.1

import requests
import urllib

from api_key import API_KEY

TEST_BASE = "https://api.steampowered.com/IDOTA2Match_205790/"
TEST_HEROES = "https://api.steampowered.com/IEconDota2_205790/"


LIVE_BASE = "https://api.steampowered.com/IDOTA2Match_570/"
LIVE_HEROES = "https://api.steampowered.com/IEconDOTA2_570/"


BASE_URL = LIVE_BASE
BASE_URL_HEROES = LIVE_HEROES


def set_api_key(key):
    """
    Set your API key for all further API queries
    """

    global API_KEY
    API_KEY = key


def url_map(base, params):
    """
    Return a URL with get parameters based on the params passed in

    @param params: HTTP GET parameters
    """

    url = base

    if '?' not in url and len(params):
        url += "?"
    elif '?' in url:
        if not url.endswith("&") and not url.endswith("?"):
            url += "&"

    for key, value in params.iteritems():
        if value is not None:
            if not isinstance(value, basestring):
                value = str(value)

            url += "%s=%s&" % (urllib.quote_plus(key.encode("utf-8")),
                               urllib.quote_plus(value.encode("utf-8")))

    if url.endswith("&") or url.endswith("?"):
        url = url[:-1]

    return str(url)


def get_page(url, count=0):
    """
    Fetch a page
    """

    import requests
    try:
#    print 'GET %s' % (url, )
        return requests.get(url)
    except Exception, e:
        print  datetime.datetime.now(), "Exception:", e, sys.exc_info()[0]
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
        print url
        time.sleep(30+count*60)
        if count < 10:
            return get_page(url, count=count+1)
        else:
            print '*'*60
            print 'Maximum count reached. Abandoning.'
            return None


def make_request_econ(name, params=None, version="V001", key=None,
                 fetcher=get_page):
    """
    Make an API request
    """

    params = params or {}
    params["key"] = key or API_KEY

    if not params["key"]:
        raise ValueError("API key not set")

    url = url_map("%s%s/%s/" % (BASE_URL_HEROES, name, version), params)
    return fetcher(url)

def make_super_request(api, name, params=None, version="V001", key=None,
                 fetcher=get_page):
    """
    Make an API request
    """

    params = params or {}
    params["key"] = key or API_KEY

    if not params["key"]:
        raise ValueError("API key not set")

    url = url_map("%s%s/%s/" % ("https://api.steampowered.com/" + api + "/", name, version), params)
    return fetcher(url)


def make_request(name, params=None, version="V001", key=None,
                 fetcher=get_page):
    """
    Make an API request
    """

    params = params or {}
    params["key"] = key or API_KEY

    if not params["key"]:
        raise ValueError("API key not set")

    url = url_map("%s%s/%s/" % (BASE_URL, name, version), params)
    return fetcher(url)


def get_hero_list(language="en_us"):
    """
    List of heroes
    """

    time.sleep(SLEEP_DELAY)

    return make_request_econ("GetHeroes", {"language": language})


def json_match_history(**kwargs):
    json = get_match_history(**kwargs)
    if json != None:
        return json.json()
    else:
        return { }



def get_match_history(start_at_match_id=None, player_name=None, hero_id=None,
                      skill=0, date_min=None, date_max=None, account_id=None,
                      league_id=None, matches_requested=None,
                      **kwargs):
    """
    List of most recent 25 matches before start_at_match_id
    """

    time.sleep(SLEEP_DELAY)

    params = {
        "account_id": account_id,
        "start_at_match_id": start_at_match_id,
        "player_name": player_name,
        "hero_id": hero_id,
        "skill": skill,
        "date_min": date_min,
        "date_max": date_max,
        "league_id": league_id,
        "matches_requested": matches_requested,
    }

    return make_request("GetMatchHistory", params, **kwargs)

def get_match_details(match_id, **kwargs):
    """
    Detailed information about a match
    """

    time.sleep(SLEEP_DELAY)

    return make_request("GetMatchDetails", {"match_id": match_id}, **kwargs)

def json_match_details(match_id, **kwargs):
    json = get_match_details(match_id, **kwargs)
    if json != None:
        return json.json()
    else:
        return {}

