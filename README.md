# @pi-watch

## Get inspired

[Nicole He](https://twitter.com/nicolehe) made a pretty cool thing where she has a Raspberry Pi take a photo of a house plant with a webcam once a day and tweet it. The Twitter account is [@grow_slow](http://twitter.com/grow_slow) and she explains a bit about the project [here](http://nicole.pizza/grow_slow). Additional awesomeness is that she documented everything and put the details up on [GitHub](https://github.com/nicolehe/grow_slow).

This is my project inspired by, and building on top of, what she did. I have the webcam take pictures throughout a day and then tweet a timelapse GIF of the day via [@pi_watch](https://twitter.com/pi_watch).

_**I'm still working on making my instructions as comprehensive and beginner-friendly as Nicole. And I also have some TODOs before I would consider my script "complete".**_

## Get things

 I ordered my hardware from [Adafruit](https://www.adafruit.com/) but there are plenty of places to buy the components.

item | cost | link
--- | --- | ---
Raspberry Pi 3 - Model B | $39.95 | [link](https://www.adafruit.com/product/3055)
Adafruit Raspberry Pi case - smoke base w/ clear top^ | $7.95 | [link](https://www.adafruit.com/product/2258)
USB WiFi (802.11b/g/n) module with antenna^^ | $19.95 | [link](https://www.adafruit.com/product/1030)
5V 1A (1000mA) USB port power supply^^^ | $5.95 | [link](https://www.adafruit.com/product/501)
USB cable - A/MicroB - 3ft | $2.95 | [link](https://www.adafruit.com/product/592)
USB webcam^^^^ | n/a | n/a
micro SD card, 16GB^^^^^ | n/a | n/a

^ You could also build your own case, or go without. I'm pleased with the one I purchased.

^^ There are cheaper USB wifi modules but I went for one with a better antenna because I wasn't sure how much building was going to be between the internet router and my Pi.

^^^ Adafruit also sells a [power supply](https://www.adafruit.com/product/1995) that has an integrated cable but it was out of stock when I ordered.

^^^^ I already had a Logitech C170 USB webcam lying around.

^^^^ I already had a spare micro SD card lying around.

## Get the OS installed

There are [instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) available for using Etcher, a graphical SD card writing tool. I followed the [command line instructions](https://www.raspberrypi.org/documentation/installation/installing-images/mac.md) for OSX.

- I downloaded [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/)
- Unzipped the Raspbian download
- Using a micro-SD card adapter, I plugged my micro-SD card into my computer
- Using Disk Utility I formatted my SD card with format `MS-DOS(FAT)`
- Opened terminal
- `diskutil list` and noted that the SD card was `disk2`
- `diskutil unmountDisk /dev/disk2`
- `cd Downloads`
- `sudo dd bs=1m if=2017-09-07-raspbian-stretch-lite.img of=/dev/rdisk2 conv=sync`
- Pressed `control`+`T` to check that it was running, then waiting for the terminal prompt to return
- `cd /Volumes/boot`
- `touch ssh` (*For headless setup, SSH can be enabled by placing a file named ssh, without any extension, onto the boot partition of the SD card. When the Pi boots, it looks for the  ssh file. If it is found, SSH is enabled, and the file is deleted. The content of the file does not matter: it could contain text, or nothing at all.*)
- Eject the SD card and insert it in the Raspberry Pi

## Get the Pi ready

- Power up the Raspberry Pi
- Connect it to your Wi-Fi router via ethernet cable
- From terminal `ssh pi@raspberrypi` and wait (it can take awhile)
- If you get `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`
  - `nano /Users/danbjoseph/.ssh/known_hosts`
  - delete the line that starts with `raspberrypi` (navigate to the line and press `control`+`k`, then `control`+`x` to exit, then `Y` to save changes, then `enter` to confirm the file name)
- Wait for the password prompt and enter `raspberry`, the default login is user: `pi` | pass: `raspberry`
- `passwd` and followed instructions to set a new password
- `python --version` on my Pi showed `Python 2.7.13`
- `sudo apt-get update`
- `sudo apt-get install fswebcam`
- `sudo apt-get install imagemagick`
- `sudo apt-get install git`
- `sudo apt-get install python-setuptools`
- `sudo apt-get install python-pip`
- `sudo pip install pytz`
- `sudo pip install tzlocal`
- `sudo pip install twython`
- `sudo pip install ephem`
- `wpa_passphrase "network_ssid" "network_password" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null` to setup [Wi-Fi](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)
- `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`
- I changed `county=GB` to `country=US` and deleted the line with the visible password
- At this point you should be able to disconnect the ethernet cable
- `git clone `
- `sudo git clone https://github.com/danbjoseph/twitter-daily-timelapse.git`
- `sudo chown -R pi /home/pi/twitter-daily-timelapse/` (when running the script as the `pi` user, this should let it create the new folder each day)
-  can test webcam with `fswebcam -d /dev/video0 -r1024x768 --no-banner -S30 -F2 test.jpg`
- `sudo rm test.jpg`

- need to turn your Pi off while connected to it via ssh? `sudo shutdown -h now`


## Setup twitter

- Already have a twitter account with my_email@gmail.com? You can use my_email+whatever@gmail.com to sign up for another account and the confirmation email will still be routed to you.


## Prepare the Python script

- Need to edit these lines
```
CONSUMER_KEY = 'your consumer key here'
CONSUMER_SECRET = 'your consumer secret here'
ACCESS_KEY = 'your access key here'
ACCESS_SECRET = 'your access secret here'
```
- And change these details as well
```
LAT = 38.8964
LNG = -77.0458
TZ = 'US/Eastern'
```


## Make it cron

- RaspberryPi.org explanation about how [cron](https://www.raspberrypi.org/documentation/linux/usage/cron.md)
- I had a heck of time getting my python script to run with cron, a task scheduler
- `crontab -e`
- addede to the top of the file (to run it every 10 minutes)
```
PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin
SHELL=/bin/bash
*/10 * * * * python /home/pi/twitter-daily-timelapse/twitter-timelapse.py
```
- troubleshooting...
  - I read that `env -i /bin/bash --noprofile --norc`  will switch you into the same  environment as the one used by crontab, then you can run your python script and see why it fails
  - You can check what shell crontab is using by printing out the environment variables from a dummy job `* * * * * env > /tmp/env.output` then `sudo nano /tmp/env.output` to look at the contents, as suggested [here](https://askubuntu.com/questions/23009/why-crontab-scripts-are-not-working)
  - Mine showed `SHELL=/bin.sh` so i set the shell to bash by adding `SHELL=/bin/bash` to the top of my crontab


## Optionally set a reboot


## Potential issues

- The Twitter API will return a 400 (Bad Request) if your image file size isn't <= 5242880 bytes, you can change the frequency of the cron schedule or adjust the compression % when creating the GIF (with the `-resize 25%` parameter)

## Position your webcam, and then do whatever you want

If you do something with my code, please continue to credit [Nicole He](https://twitter.com/nicolehe) and let her know. Especially if you help her get one step closer to being the instigator of an internet garden. :seedling::seedling::seedling: