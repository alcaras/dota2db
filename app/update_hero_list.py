# update the hero list


from db import session
from models import *

from api import *
import pprint
pp = pprint.PrettyPrinter(indent = 4)

print "hello from the hero list updater"

print "clearing existing hero list..."
heroes = session.query(Hero).all()
for a in heroes:
    session.delete(a)

print "getting new hero list..."

req = get_hero_list()

hero_json = req.json()

#pp.pprint(hero_json)


print "Found", len(hero_json["result"]["heroes"]), "heroes"

for a in hero_json["result"]["heroes"]:
    new_hero = Hero(a["id"], a["localized_name"], a["name"])
    session.add(new_hero)
    print "Added", new_hero

session.commit()
print "Done!"


