#!/usr/bin/env python2

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, HTTPError, URLError
import requests
import cStringIO
import Image


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
            return
        background = Image.open("basemap.jpg")
        foreground = foreground.convert('RGBA')
        background.paste(foreground, (0, 0), foreground)
        # background = background.convert('P')
        background.save(out_folder + filename)

if __name__ == "__main__":
    import os
    RADARSITE = 'http://radar.weather.gov/ridge/RadarImg/N1P/DGX/'
    IMAGEPATH = os.path.expanduser('~/Projects/weather/images/')
    for f in [IMAGEPATH + f for f in os.listdir(IMAGEPATH) if f.endswith(".gif")]:
        os.remove(f)
    get_radar(RADARSITE, IMAGEPATH)
