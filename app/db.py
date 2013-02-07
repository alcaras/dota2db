from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pdb
import os

# change to our current directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

engine = create_engine('sqlite:///db.db', echo=False)

# create a Session
Session = sessionmaker(bind=engine)
session = Session()
