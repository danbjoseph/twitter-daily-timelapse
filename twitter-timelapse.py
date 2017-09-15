#!/usr/bin/env python
import sys
import os
import time
import ephem
from datetime import datetime
import pytz
from twython import Twython
import shutil

# regardless of where we run the script, we want things
# to happen in the same folder as the script itself
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# we need to be able to access Twitter
# go here and create a new app: https://apps.twitter.com
# then click "key and access tokens" to generate them
# put them inside the quotes below
CONSUMER_KEY = 'your consumer key here'
CONSUMER_SECRET = 'your consumer secret here'
ACCESS_KEY = 'your access key here'
ACCESS_SECRET = 'your access secret here'

# put in your own details here
LAT = 38.8964
LNG = -77.0458
TZ = 'US/Eastern'


local_tz = pytz.timezone(TZ)
utc_now = datetime.utcfromtimestamp(time.time())
local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)
local_noon = local_now.replace(hour=12, minute=00)
today_dir = datetime.strftime(local_now, '%Y-%m-%d')

# make a pyephem observer
my_location = ephem.Observer()
my_location.lat, my_location.lon = str(LAT), str(LNG)
# pyephem takes and returns UTC times but we dont care about the time
# we want the date in the current timezone so we will pass the
# local time and let pyephem ignore the timezone
my_location.date = local_noon
# my_location.elev = 20 # elevation of in meters
# to get U.S. Naval Astronomical Almanac values, use these settings
my_location.pressure = 0
my_location.horizon = '-0:34'
# relocate the horizon to get twilight times
my_location.horizon = '-6' # -6=civil twilight, -12=nautical, -18=astronomical
# calculate then convert pyephem date to a Python datetime object and attach timezone info
beg_twilight = my_location.previous_rising(ephem.Sun(), use_center=True).datetime().replace(tzinfo=pytz.utc).astimezone(local_tz)
end_twilight = my_location.next_setting(ephem.Sun(), use_center=True).datetime().replace(tzinfo=pytz.utc).astimezone(local_tz)

print local_now
print beg_twilight
print end_twilight

if local_now > end_twilight:
    print "It's after sunset!"
    # if the folder still exists for today
    if os.path.exists(today_dir):
        # make a GIF of today's images and tweet
        # https://www.imagemagick.org/script/command-line-options.php
        os.system ("convert -resize 25% -delay 10 -loop 0 " + today_dir + "/*.jpg " + today_dir + ".gif")
        api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)
        photo = open(today_dir + '.gif','rb')
        image_ids = api.upload_media(media=photo)
        api.update_status(status='', media_ids=image_ids['media_id'])
        # TODO: delete the gif
        # ...
        # zip the folder of images
        shutil.make_archive(today_dir, 'zip', today_dir)
        # TODO: save zip to S3 and then delete the zip
        # ...
        # delete the folder
        shutil.rmtree(today_dir)
elif local_now > beg_twilight:
    print "It's daytime!"
    now_img = datetime.strftime(local_now, '%Y-%m-%d_%H-%M');
    # this creates a folder for today's images if it doesn't exist
    if not os.path.exists(today_dir):
        os.makedirs(today_dir)
        # uid = pwd.getpwnam("pi").pw_uid
        # os.chown(today_dir, uid, -1);
    # take a picture and save to folder for today
    # fswebcam works for USB webcams, if you're using
    # a Pi camera module you'll need something different
    os.system ("fswebcam -d /dev/video0 -r1024x768 --no-banner -S30 -F2 " + today_dir + "/" + now_img + ".jpg")
else:
    print "It's before dawn still. Good bye!"
