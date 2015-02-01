from flask import Flask
from flask import request
from flask import redirect
from flask import render_template, url_for

from common import get_tweet
from common import generate_image

app = Flask(__name__)
# app.config['STATIC_FOLDER'] = 'twitter'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        tweet_id = request.form['tweet_id']
        if not tweet_id:
            return render_template('index.html')

        tweet = get_tweet(tweet_id)
        file_id = generate_image(tweet.AsDict())
        return redirect(url_for('index', id=file_id))


if __name__ == '__main__':
    app.run(port=8001)
