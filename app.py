import os

from flask import Flask
from flask import url_for
from flask import request
from flask import redirect
from flask import send_file
from flask import render_template
from flask import send_from_directory

from database.db import db
from database.models import Tweet

from common import get_tweet
from common import generate_image

from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

port = 8001


@app.route('/', methods=['GET'])
def index_get():
    existing_items = Tweet.query.order_by(Tweet.created.desc()).limit(10)
    existing_items = [x.tweet_id for x in existing_items]
    print 'here'
    return render_template('index.html', existing_items=existing_items, request=request)


@app.route('/', methods=['POST'])
def index_post():
    tweet_id = request.form['tweet_id']
    if not tweet_id:
        return render_template('index.html')

    tweet_entry = Tweet.query.get(int(tweet_id))
    if tweet_entry:
        now = datetime.now()
        tweet_entry.created = now
        db.session.commit()
        return redirect(url_for('index_get', id=tweet_id))

    tweet = get_tweet(tweet_id).AsDict()
    db.session.add(Tweet(tweet))
    db.session.commit()
    return redirect(url_for('index_get', id=tweet_id))


@app.route('/generate/<tweet_id>', methods=['GET'])
def generate_get(tweet_id):
    tweet = get_tweet(tweet_id)
    file_io = generate_image(tweet.AsDict())
    return send_file(file_io, attachment_filename='image.jpeg')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    with app.test_request_context():
        db.create_all()

    app.run(port=port)
