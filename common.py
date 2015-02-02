import os
import time
import twitter

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

cwd = os.path.dirname(os.path.realpath(__file__))
img_path = os.path.join(cwd, 'static', 'img', 'backgrounds', 'priroda-leto-rasteniya-zelen.jpg')
out_dir = os.path.join(cwd, 'static', 'img', 'created')
georgia_calligraphy_path = os.path.join(cwd, 'fonts', 'Georgia_Italic.ttf')
calibri_path = os.path.join(cwd, 'fonts', 'Calibri.ttf')

# Make sure out_dir exists
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


# I did not write this function. Credit:
# https://mail.python.org/pipermail/image-sig/2004-December/003064.html
def intelli_draw(drawer, text, font, container_width):
    words = text.split()
    lines = []
    lines.append(words)
    finished = False
    line = 0
    while not finished:
        thistext = lines[line]
        newline = []
        inner_finished = False
        while not inner_finished:
            if drawer.textsize(' '.join(thistext), font)[0] > container_width:
                newline.insert(0, thistext.pop(-1))
            else:
                inner_finished = True
        if len(newline) > 0:
            lines.append(newline)
            line = line + 1
        else:
            finished = True
    tmp = []
    for i in lines:
        tmp.append(' '.join(i))
    lines = tmp
    (width, height) = drawer.textsize(lines[0], font)
    return (lines, width, height)


def stroke(draw, x, y, line, font, size):
    draw.text(xy=(x - size, y), text=line, font=font, fill='black')
    draw.text(xy=(x + size, y), text=line, font=font, fill='black')
    draw.text(xy=(x, y - size), text=line, font=font, fill='black')
    draw.text(xy=(x, y + size), text=line, font=font, fill='black')


def generate_image(tweet):
    font_size = 100
    margin = 30
    padding_left = 1150

    image = Image.open(img_path)
    draw = ImageDraw.Draw(image)
    lucida_calligraphy = ImageFont.truetype(georgia_calligraphy_path, font_size)
    helvetica = ImageFont.truetype(calibri_path, int(font_size * .75))
    helvetica_small = ImageFont.truetype(calibri_path, int(font_size * .5))

    image_width, image_height = image.size
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))

    lines, w, h = intelli_draw(draw, tweet['text'], lucida_calligraphy, image_width - (margin * 2) - padding_left)
    for i, line in enumerate(lines):

        # Calculate x and y
        x = margin + padding_left
        y = i * h

        # Draw the line
        stroke(draw, x, y, line, lucida_calligraphy, 5)
        draw.text(xy=(x, y), text=line, font=lucida_calligraphy, fill='white')

    # Draw the username
    at_username = '@' + tweet['user']['screen_name']
    username_width, username_height = draw.textsize(at_username, helvetica)
    x = margin
    y = image_height - username_height - margin
    stroke(draw, x, y, at_username, helvetica, 2)
    draw.text(xy=(x, y), text=at_username, font=helvetica)

    # Draw the timestamp
    timestamp_width, timestamp_height = draw.textsize(timestamp, helvetica_small)
    x = username_width + (margin * 2)
    y = image_height - margin - (timestamp_height * 1.3)
    stroke(draw, x, y, timestamp, helvetica_small, 2)
    draw.text(xy=(x, y), text=timestamp, font=helvetica_small)

    # Write out the image
    file_name = '{}.jpg'.format(tweet['id'])
    file_path = os.path.join(out_dir, file_name)
    image.save(file_path)

    return tweet['id']


def get_tweet(tweet_id):
    tweet_id = int(tweet_id)
    api = twitter.Api(
        consumer_key=os.environ['twitter_consumer_key'],
        consumer_secret=os.environ['twitter_consumer_secret'],
        access_token_key=os.environ['twitter_access_token_key'],
        access_token_secret=os.environ['twitter_access_token_secret'])
    return api.GetStatus(tweet_id)
