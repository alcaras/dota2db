from migrate.versioning import api
from db import engine, session
from models import Match, Player
import os.path
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

Match.metadata.create_all(engine)
Player.metadata.create_all(engine)
 
