#!/usr/bin/env python2

import Image
import os
import gifmaker
from images2gif import writeGif


giflist = list()
image_path = os.path.expanduser("~/Projects/weather/images/")
for image in os.listdir(image_path):
    if not image.endswith('.gif'):
        continue
    background = Image.open("basemap.jpg")
    foreground = Image.open(image_path + image)
    foreground = foreground.convert('RGBA')
    background.paste(foreground, (0, 0), foreground)
    background = background.convert('P')
    giflist.append(background)

writeGif(os.path.expanduser('~/Projects/weather/radar.gif'), giflist)
fp = open(os.path.expanduser('~/Projects/weather/radar.gif'), 'wb')
gifmaker.makedelta(fp, giflist)
fp.close()
