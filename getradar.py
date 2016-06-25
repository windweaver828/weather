#!/usr/bin/env python2

from bs4 import BeautifulSoup
from urllib2 import urlopen, Request, HTTPError, URLError
from urllib import urlretrieve


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
        outpath = IMAGEPATH + filename
        try:
            urlretrieve(imageurl, outpath)
        except Exception as e:
            print(e)
            print "skipping" + imageurl

if __name__ == "__main__":
    import os
    RADARSITE = 'http://radar.weather.gov/ridge/RadarImg/N1P/DGX/'
    IMAGEPATH = os.path.expanduser('~/Projects/weather/images/')
    get_radar(RADARSITE, IMAGEPATH)
