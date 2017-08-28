import sys
import os
from datetime import datetime
from twython import Twython
import pytz
from sunrise_sunset import SunriseSunset
# https://github.com/jebeaudet/SunriseSunsetCalculator
import shutil

# go here and create a new app: https://apps.twitter.com
# then click "key and access tokens" to generate them
# put them inside the quotes below
CONSUMER_KEY = 'your consumer key here'
CONSUMER_SECRET = 'your consumer secret here'
ACCESS_KEY = 'your access key here'
ACCESS_SECRET = 'your access secret here'

ro = SunriseSunset(datetime.now(), latitude=38.8964,longitude=-77.0458)
sunrise, sunset = ro.calculate()
sunrise = pytz.timezone('UTC').localize(sunrise)
sunset = pytz.timezone('UTC').localize(sunset)
dt = pytz.timezone('US/Eastern').localize(datetime.now())
today_dir = datetime.strftime(dt, '%Y-%m-%d');

# # testing
# os.system ("convert -delay 20 -loop 0 " + today_dir + "/*.jpg " + today_dir + ".gif")
# shutil.make_archive(today_dir, 'zip', today_dir)


if dt > sunset:
    print "It's after sunset!"
    # if the folder still exists for today
    if os.path.exists(today_dir):
        # make a GIF of today's images and tweet
        # https://www.imagemagick.org/script/command-line-options.php
        os.system ("convert -resize 30% -delay 10 -loop 0 " + today_dir + "/*.jpg " + today_dir + ".gif")
        api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
        photo = open(today_dir + '.gif','rb')
        image_ids = api.upload_media(media=photo)
        api.update_status(status='', media_ids=image_ids['media_id'])
        # delete the gif
        # ...
        # zip the folder of images
        shutil.make_archive(today_dir, 'zip', today_dir)
        # save zip to S3
        # ...
        # delete the folder
        shutil.rmtree(today_dir)
elif dt > sunrise:
    print "It's daytime!"
    now_img = datetime.strftime(dt, '%Y-%m-%d_%H-%M');
    # this creates a folder for today's images if it doesn't exist
    if not os.path.exists(today_dir):
        os.makedirs(today_dir)
    # take a picture and save to folder for today
    # fswebcam works for USB webcams, if you're using
    # a Pi camera module you'll need something different
    os.system ("fswebcam -d /dev/video0 -r1024x768 --no-banner -S30 -F2 " + today_dir + "/" + now_img + ".jpg")
else:
    print "It's before dawn still. Good bye!"
