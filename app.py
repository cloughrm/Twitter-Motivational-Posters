import os
import sys
import glob

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template, url_for

from common import get_tweet
from common import generate_image

app = Flask(__name__)
port = 8001
IMAGES_GLOB = os.path.join('static', 'img', 'created', '*.jpg')


def get_latest(folder):
    files = glob.glob(folder)
    for f in files:
        print os.path.getmtime(f), f
    files.sort(key=lambda x: os.path.getmtime(x))
    files.reverse()
    files = [os.path.basename(x).split('.')[0] for x in files[:10]]
    return files


@app.route('/', methods=['GET', 'POST'])
def index():
    scope = {}

    # GET request
    if request.method == 'GET':
        scope['existing_images'] = get_latest(IMAGES_GLOB)
        return render_template('index.html', scope=scope)

    # POST request
    tweet_id = request.form['tweet_id']
    if not tweet_id:
        return render_template('index.html')

    tweet = get_tweet(tweet_id)
    file_id = generate_image(tweet.AsDict())
    return redirect(url_for('index', id=file_id))


if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == 'dev':
        debug = True
    app.run(port=port, debug=debug)
