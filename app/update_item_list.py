# update the hero list

import pdb
from db import session
from models import *
import sys

import re

from api import *
import pprint
pp = pprint.PrettyPrinter(indent = 4)

print "hello from the item list updater"

#print "clearing existing item list..."
#items = session.query(Item).all()
#for a in items:
#    session.delete(a)

print "reading new item list..."
f = open('extracted/items.txt', 'r')
data = f.read()
data = data.replace('\r', '')

regex = '\/\/(?:=)+$(?:\s*)\/\/(?:\s*)([\w\s]*)$(?:\s*)\/\/(?:=)+$(?:\s*)"item_(\w*)"$(?:\s)*{$(?:\s*)\/\/ General$(?:\s*)\/\/[-]*$(?:\s*)"ID"(?:\s)*"(\d*)"'

match = re.findall(regex, data, re.M)


pp.pprint(match)
for a in match:
    new_item = Item(a[2], a[0], a[1])
    session.add(new_item)
    print "Added", new_item 

session.commit()
print "Done!"


