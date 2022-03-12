from datetime import datetime

from database.db import db


class Tweet(db.Model):
    tweet_id = db.Column(db.Integer, primary_key=True)
    tweet_text = db.Column(db.String(140))
    user = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime())
    created = db.Column(db.DateTime())

    def __init__(self, tweet):
        self.tweet_id = tweet['data']['id']
        self.tweet_text = tweet['data']['text']
        self.user = tweet['includes']['users'][0]['username']
        self.timestamp = datetime.strptime(tweet['data']['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.created = datetime.now()

    def __repr__(self):
        return '<Tweet {}>'.format(self.tweet_id)
