#!/usr/bin/env python2
#
#  Non-Interactive Weather Display (NIWD)
#  Copyright (C) 2016  Keith Brandenburg
#  Copyright (C) 2016  James Upton
#
#  This file is part of NIWD

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, HTTPError, URLError
import requests
import cStringIO
import Image
import os


def make_soup(url):
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    html = None
    while not html:
        try:
            html = urlopen(req).read()
        except HTTPError:
            print("HTTPError... Retrying")
            html = None
        except URLError:
            print("Connection error.. Skipping - {}".format(url))
            return False

    return BeautifulSoup(html, "lxml")


def get_radar(url, out_folder):
    soup = make_soup(url)
    for image in soup.findAll("a"):
        filename = image['href']
        if not filename.endswith('.gif'):
            continue
        imageurl = url + filename
        response = requests.get(imageurl)
        try:
            foreground = Image.open(cStringIO.StringIO(response.content))
        except Exception as e:
            print(e)
            print "skipping " + imageurl
            continue
        background = Image.open(os.path.expanduser('~/Projects/weather/basemap.jpg'))
        foreground = foreground.convert('RGBA')
        background.paste(foreground, (0, 0), foreground)
        background.save(out_folder + filename)


def run():
    import apt

    if not apt.Cache()['imagemagick'].is_installed:
        import sys
        print("Do sudo apt-get install imagemagick to use this script.")
        sys.exit(1)
    RADARSITE = 'http://radar.weather.gov/ridge/RadarImg/N1P/MOB/'
    IMAGEPATH = os.path.expanduser('~/Projects/weather/images/')
    GIFPATH = os.path.expanduser("~/Projects/weather/radar.gif")
    for f in [IMAGEPATH + f for f in os.listdir(IMAGEPATH) if f.endswith(".gif")]:
        os.remove(f)
    get_radar(RADARSITE, IMAGEPATH)
    command = "convert -delay 20 -loop 0 {}*.gif {}".format(IMAGEPATH, GIFPATH)
    os.system(command)

if __name__ == "__main__":
    run()
