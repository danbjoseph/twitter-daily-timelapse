# work in progress still
# @pi-watch

[Nicole He](https://twitter.com/nicolehe) made a pretty cool thing where she has a Raspberry Pi take a photo of a house plant with a webcam once a day and tweet it. The Twitter account is [@grow_slow](http://twitter.com/grow_slow) and she explains a bit about the project [here](http://nicole.pizza/grow_slow). Additional awesomeness is that she documented everything and put the details up on [GitHub](https://github.com/nicolehe/grow_slow).

This is my project inspired by, and building on top of, what she did. Some of the instructions are copied/pasted from her instructional README.

## Get things

I already had a Logitech C170 USB webcam lying around. I ordered the rest of my hardware from [Adafruit](https://www.adafruit.com/) but there are plenty of places to buy the components.
```plain
Raspberry Pi 3 - Model B^ | $39.95 | [link](https://www.adafruit.com/product/3055)
Adafruit Raspberry Pi Case - Smoke Base w/ Clear Top^^ | $7.95 | [link](https://www.adafruit.com/product/2258)
USB WiFi (802.11b/g/n) Module with Antenna | $19.95 | [link](https://www.adafruit.com/product/1030)
5V 1A (1000mA) USB port power supply^^^ | $5.95 | [link](https://www.adafruit.com/product/501)
USB cable - A/MicroB - 3ft | $2.95 | [link](https://www.adafruit.com/product/592)
```
^ You could build your own case, or go without. I'm pleased with the one I purchased.
^^ There are cheaper USB wifi modules but I went for one with a better antenna because I wasn't sure how much building was going to be between the internet router and my Pi.
^^^ Adafruit also sells a [power supply](https://www.adafruit.com/product/1995) that has an integrated cable but it was out of stock when I ordered.

## Setup the Pi
```
$ python --version
Python 2.7.13
```

## Connect to wifi

## Setup ssh

When going through things the first time I followed:
https://www.raspberrypi.org/documentation/remote-access/ssh/

TODO: For headless setup, SSH can be enabled by placing a file named ssh, without any extension, onto the boot partition of the SD card. When the Pi boots, it looks for the  ssh file. If it is found, SSH is enabled, and the file is deleted. The content of the file does not matter: it could contain text, or nothing at all.

## Connect via ssh
can unplug from your monitor and keyboard now
nmap as described here https://www.raspberrypi.org/documentation/remote-access/ip-address.md didn't work for me


## Set the date

Now that your Pi is up and running, open the Terminal from the toolbar at the top, or log in via SSH. You should see something that looks like this:

`pi@raspberrypi ~ $`

We're going to set the date so that our Pi is on the right time.

Type this in and press enter:

`date`

You should get something formatted like "Wed 6 Jun 20:11:24 EDT 2016." And if it's correct, then hooray, you don't have to do anything else. If it's not, enter:

`tzselect`

and follow the instructions to set your timezone. Once you've done it you can confirm by entering `date` again and it should be correct.

## Setup the webcam

## Install dependencies

## Setup twitter

## Prepare the Python script

## Make it cron

To do this, we'll use something called cron, which is basically a task scheduler. [RaspberryPi.org has some good explanation about how this works](https://www.raspberrypi.org/documentation/linux/usage/cron.md).

Let's open up our crontab: `crontab -e`

This is the structure of the crontab:

```
# m h  dom mon dow   command
# * * * * *  command to execute
# ┬ ┬ ┬ ┬ ┬
# │ │ │ │ │
# │ │ │ │ │
# │ │ │ │ └───── day of week (0 - 7) (0 to 6 are Sunday to Saturday, or use names; 7 is Sunday, the same as 0)
# │ │ │ └────────── month (1 - 12)
# │ │ └─────────────── day of month (1 - 31)
# │ └──────────────────── hour (0 - 23)
# └───────────────────────── min (0 - 59)
```

## Optional but recommended: set a reboot


## Position your webcam, and then do whatever you want

If you do something with my code, please continue to credit [Nicole He](https://twitter.com/nicolehe) and let her know. Especially if you help her get one step closer to being the instigator of an internet garden. :seedling::seedling::seedling: