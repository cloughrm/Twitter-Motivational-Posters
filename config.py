import os
import sys

from dotenv import load_dotenv
load_dotenv()

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///database/sqlite.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', None)
if not TWITTER_BEARER_TOKEN:
	print('TWITTER_BEARER_TOKEN not set')
	sys.exit()