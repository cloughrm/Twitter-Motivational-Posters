from datetime import datetime

from db import db


class Tweet(db.Model):
    tweet_id = db.Column(db.Integer, primary_key=True)
    tweet_text = db.Column(db.String(140))
    user = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime())
    created = db.Column(db.DateTime())

    def __init__(self, tweet):
        self.tweet_id = tweet['id']
        self.tweet_text = tweet['text']
        self.user = tweet['user']['screen_name']
        self.timestamp = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
        self.created = datetime.now()

    def __repr__(self):
        return '<Tweet {}>'.format(self.tweet_id)
