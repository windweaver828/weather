#!/usr/bin/env python2
#
#  Non-Interactive Weather Display (NIWD)
#  Copyright (C) 2016  Keith Brandenburg
#  Copyright (C) 2016  James Upton
#
#  This file is part of NIWD
#
#  NIWD is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  NIWD is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with NIWD.  If not, see <http://www.gnu.org/licenses/>
#

from PySide import QtGui
from PySide import QtCore
import sys
import os
import time
import json
import math
import urllib2
import collections
import getradar
from colour import Color
from keith import Process


class Weather(QtGui.QGraphicsView, QtCore.QObject):
    def __init__(self, parent=None):
        super(Weather, self).__init__(parent)
        self.setStyleSheet("background: transparent; border: none; font-weight:bold; font-family:URW Chancery L ")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        font = QtGui.QFont()
        font.setPointSize(24)  # sets the font size for window
        self.layout = QtGui.QVBoxLayout()   # main window
        self.Hline = QtGui.QFrame()  # used to draw a horizontal separating line
        self.Hline.setFrameStyle(QtGui.QFrame.HLine)
        self.Hline.setMaximumSize(QtCore.QSize(99999999, 3))
        self.Hline.setStyleSheet("margin:1px; border:1px solid rgb(0, 255,  127);")
        self.layout2 = QtGui.QHBoxLayout()  # horizontal across top
        self.header = QtGui.QLabel()
        getradar.run()

        # The next line set the color font and size of text for each label can be called
        # on entire window or individual widgets ie.. labels
        self.header.setStyleSheet("font-weight:bold; font-family:Purisa; color:springgreen")
        font.setPointSize(24)  # sets the font size for label
        self.header.setText("Current Weather Conditions in Lucedale, MS")
        self.layout2.addWidget(self.header)
        self.header2 = QtGui.QLabel()
        self.header2 .setStyleSheet("font-weight:bold; font-family:Purisa; color:springgreen")
        self.header2.setText("Current Weather Conditions in Long Beach, MS")
        font.setPointSize(24)
        self.layout2.addWidget(self.header2)

        self.layout3 = QtGui.QHBoxLayout()  # horizontal for curr weather

        self.layout4 = QtGui.QVBoxLayout()  # Vertical layout for current weather
        self.layout5 = QtGui.QVBoxLayout()  # two per city location
        self.layout6 = QtGui.QVBoxLayout()  #
        self.layout7 = QtGui.QVBoxLayout()  #

        self.timelabel = QtGui.QLabel()     # Current weather labels Lucedale
        self.summary = QtGui.QLabel()       # 5 per vertical in the horizontal
        self.temperature = QtGui.QLabel()   # Doubled for two cities
        self.feelslike = QtGui.QLabel()
        self.dewpoint = QtGui.QLabel()

        self.humidity = QtGui.QLabel()
        self.wind = QtGui.QLabel()
        self.chanceofrain = QtGui.QLabel()
        self.hightemp = QtGui.QLabel()
        self.lowtemp = QtGui.QLabel()

        self.timelabelLB = QtGui.QLabel()     # Current weather labels Long Beach
        self.summaryLB = QtGui.QLabel()       # 5 per vertical in the horizontal
        self.temperatureLB = QtGui.QLabel()
        self.feelslikeLB = QtGui.QLabel()
        self.dewpointLB = QtGui.QLabel()

        self.humidityLB = QtGui.QLabel()
        self.windLB = QtGui.QLabel()
        self.chanceofrainLB = QtGui.QLabel()
        self.hightempLB = QtGui.QLabel()
        self.lowtempLB = QtGui.QLabel()

        self.layout4.addWidget(self.timelabel)
        self.layout4.addWidget(self.summary)
        self.layout4.addWidget(self.temperature)
        self.layout4.addWidget(self.feelslike)
        self.layout4.addWidget(self.dewpoint)
        self.layout5.addWidget(self.humidity)
        self.layout5.addWidget(self.wind)
        self.layout5.addWidget(self.chanceofrain)
        self.layout5.addWidget(self.hightemp)
        self.layout5.addWidget(self.lowtemp)
        self.layout6.addWidget(self.timelabelLB)
        self.layout6.addWidget(self.summaryLB)
        self.layout6.addWidget(self.temperatureLB)
        self.layout6.addWidget(self.feelslikeLB)
        self.layout6.addWidget(self.dewpointLB)
        self.layout7.addWidget(self.humidityLB)
        self.layout7.addWidget(self.windLB)
        self.layout7.addWidget(self.chanceofrainLB)
        self.layout7.addWidget(self.hightempLB)
        self.layout7.addWidget(self.lowtempLB)

        self.datelabel = QtGui.QLabel()
        font = QtGui.QFont()
        font.setPointSize(14)
        self.datelabel.setStyleSheet("font-weight:bold; font-family:Purisa; color:springgreen")
        self.datelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.datelabel.setFont(font)
        self.datelabel.setText('Today, ' + time.strftime("%B %d,%Y"))

        self.layout3.addLayout(self.layout4)     # adds vertical layouts to
        self.layout3.addLayout(self.layout5)     # horizontal layout
        self.layout3.addLayout(self.layout6)     # for displaying current weather
        self.layout3.addLayout(self.layout7)     #

        self.layout8 = QtGui.QVBoxLayout()    # Main layout for hourly weather
        self.layout9 = QtGui.QVBoxLayout()    # Hourly forecast layouts
        
        self.layoutImages = QtGui.QVBoxLayout()

        self.imagelabel = QtGui.QLabel()            # Image labels to visibly show the temps
        self.image = self.addImage('blank.jpg')     # and an animated gif for the radar
        self.spacerline = QtGui.QSpacerItem(80, 30)
        self.radarlabel = QtGui.QLabel()
        self.radar = self.addRadar('radar.gif')

        self.layoutImages.addWidget(self.datelabel)
        self.layoutImages.addWidget(self.imagelabel)
        self.layoutImages.addItem(self.spacerline)
        self.layoutImages.addWidget(self.radarlabel)

        self.layout25 = QtGui.QHBoxLayout()  # horizontal containing two verticals
        # that hold the hourly divided for two cities
        self.layout8.setAlignment(QtCore.Qt.AlignJustify)
        self.layout9.setAlignment(QtCore.Qt.AlignJustify)
        self.layout25.addLayout(self.layout8)
        self.layout25.addLayout(self.layoutImages)
        self.layout25.addLayout(self.layout9)

        self.layout.addLayout(self.layout2)  # adds header layout
        self.layout.addLayout(self.layout3)  # adds current weather layout
        self.layout.addWidget(self.Hline)
        self.layout.addLayout(self.layout25)  # adds forecast weather layout

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimer)
        self.screen = QtGui.QDesktopWidget().screenGeometry()
        self.label = QtGui.QLabel()

        # list of labels to replace for label in self.labels so that I can
        # assign text to each label individually
        self.hourlabel1 = QtGui.QLabel()
        self.hourlabel2 = QtGui.QLabel()
        self.hourlabel3 = QtGui.QLabel()
        self.hourlabel4 = QtGui.QLabel()
        self.hourlabel5 = QtGui.QLabel()
        self.hourlabel6 = QtGui.QLabel()
        self.hourlabel7 = QtGui.QLabel()
        self.hourlabel8 = QtGui.QLabel()
        self.hourlabel9 = QtGui.QLabel()
        self.hourlabel10 = QtGui.QLabel()
        self.hourlabel11 = QtGui.QLabel()
        self.hourlabel12 = QtGui.QLabel()
        self.hourlabel13 = QtGui.QLabel()
        self.hourlabel14 = QtGui.QLabel()
        self.hourlabel15 = QtGui.QLabel()
        self.hourlabel16 = QtGui.QLabel()
        self.hourlabel17 = QtGui.QLabel()
        self.hourlabel18 = QtGui.QLabel()
        self.hourlabel19 = QtGui.QLabel()
        self.hourlabel20 = QtGui.QLabel()
        self.hourlabel21 = QtGui.QLabel()
        self.hourlabel22 = QtGui.QLabel()
        self.layout8.addWidget(self.hourlabel1)
        self.layout8.addWidget(self.hourlabel2)
        self.layout8.addWidget(self.hourlabel3)
        self.layout8.addWidget(self.hourlabel4)
        self.layout8.addWidget(self.hourlabel5)
        self.layout8.addWidget(self.hourlabel6)
        self.layout8.addWidget(self.hourlabel7)
        self.layout8.addWidget(self.hourlabel8)
        self.layout8.addWidget(self.hourlabel9)
        self.layout8.addWidget(self.hourlabel10)
        self.layout8.addWidget(self.hourlabel11)
        self.layout8.addWidget(self.hourlabel12)
        self.layout8.addWidget(self.hourlabel13)
        self.layout8.addWidget(self.hourlabel14)
        self.layout8.addWidget(self.hourlabel15)
        self.layout8.addWidget(self.hourlabel16)
        self.layout8.addWidget(self.hourlabel17)
        self.layout8.addWidget(self.hourlabel18)
        self.layout8.addWidget(self.hourlabel19)
        self.layout8.addWidget(self.hourlabel20)
        self.layout8.addWidget(self.hourlabel21)
        self.layout8.addWidget(self.hourlabel22)

        self.hourlabel1LB = QtGui.QLabel()
        self.hourlabel2LB = QtGui.QLabel()
        self.hourlabel3LB = QtGui.QLabel()
        self.hourlabel4LB = QtGui.QLabel()
        self.hourlabel5LB = QtGui.QLabel()
        self.hourlabel6LB = QtGui.QLabel()
        self.hourlabel7LB = QtGui.QLabel()
        self.hourlabel8LB = QtGui.QLabel()
        self.hourlabel9LB = QtGui.QLabel()
        self.hourlabel10LB = QtGui.QLabel()
        self.hourlabel11LB = QtGui.QLabel()
        self.hourlabel12LB = QtGui.QLabel()
        self.hourlabel13LB = QtGui.QLabel()
        self.hourlabel14LB = QtGui.QLabel()
        self.hourlabel15LB = QtGui.QLabel()
        self.hourlabel16LB = QtGui.QLabel()
        self.hourlabel17LB = QtGui.QLabel()
        self.hourlabel18LB = QtGui.QLabel()
        self.hourlabel19LB = QtGui.QLabel()
        self.hourlabel20LB = QtGui.QLabel()
        self.hourlabel21LB = QtGui.QLabel()
        self.hourlabel22LB = QtGui.QLabel()
        self.layout9.addWidget(self.hourlabel1LB)
        self.layout9.addWidget(self.hourlabel2LB)
        self.layout9.addWidget(self.hourlabel3LB)
        self.layout9.addWidget(self.hourlabel4LB)
        self.layout9.addWidget(self.hourlabel5LB)
        self.layout9.addWidget(self.hourlabel6LB)
        self.layout9.addWidget(self.hourlabel7LB)
        self.layout9.addWidget(self.hourlabel8LB)
        self.layout9.addWidget(self.hourlabel9LB)
        self.layout9.addWidget(self.hourlabel10LB)
        self.layout9.addWidget(self.hourlabel11LB)
        self.layout9.addWidget(self.hourlabel12LB)
        self.layout9.addWidget(self.hourlabel13LB)
        self.layout9.addWidget(self.hourlabel14LB)
        self.layout9.addWidget(self.hourlabel15LB)
        self.layout9.addWidget(self.hourlabel16LB)
        self.layout9.addWidget(self.hourlabel17LB)
        self.layout9.addWidget(self.hourlabel18LB)
        self.layout9.addWidget(self.hourlabel19LB)
        self.layout9.addWidget(self.hourlabel20LB)
        self.layout9.addWidget(self.hourlabel21LB)
        self.layout9.addWidget(self.hourlabel22LB)

        self.layout.addLayout(self.layout2)
        self.header.setFont(font)
        self.header2.setFont(font)
        self.setLayout(self.layout)
        self.setGeometry(0, 0, (self.screen.width()), (self.screen.height()))
        self.weather_dict = {}
#        self.timer.start(5000)
        self.onTimer()

    def addRadar(self, fname):
        self.movie = QtGui.QMovie(fname, QtCore.QByteArray(), self)
        self.movie.setScaledSize(QtCore.QSize(400, 300))
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.setSpeed(100)
        self.radarlabel.setMovie(self.movie)
        self.radarlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.movie.start()

    def addImage(self, image):
        self.image = 'WeatherIcons' + os.sep + image
        self.pixmap = QtGui.QPixmap(self.image).scaled(400, 175, QtCore.Qt.KeepAspectRatio)
        self.imagelabel.setPixmap(self.pixmap)
        self.imagelabel.setAlignment(QtCore.Qt.AlignCenter)
        self.layoutImages.addWidget(self.imagelabel)

    def onTimer(self):
        QtGui.QApplication.processEvents()
        blue1 = Color('#6a9dcf')
        blue2 = Color('#1D2951')
        colors = list(blue1.range_to(blue2, 50))
        self.skipped = False
        for location, x in LOCATIONS.items():
            lat, lng = x
            self.weather_list = self.get_weather(location, lat, lng)
            self.current_weather = self.weather_list[0]
            self.hour1 = self.weather_list[1]
            self.hour2 = self.weather_list[2]
            self.hour3 = self.weather_list[3]
            self.hour4 = self.weather_list[4]
            self.hour5 = self.weather_list[5]
            self.hour6 = self.weather_list[6]
            self.hour7 = self.weather_list[7]
            self.hour8 = self.weather_list[8]
            self.hour9 = self.weather_list[9]
            self.hour10 = self.weather_list[10]
            self.hour11 = self.weather_list[11]
            self.space1 = '\t\t'
            self.space2 = '\t\t\t'
            self.space3 = '\t\t\t'

            # check if hour ==  23 if so populate a dividerdatelabel(has to be made first) to separate today from tommorow
            if self.current_weather['location'] == 'Lucedale':
                self.timelabel.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.timelabel.setText(time.strftime("%I:%M %p"))
                self.summary.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.summary.setText(self.current_weather['Conditions'])
                self.temperature.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.temperature.setText('Temp: ' + str(self.current_weather['Temperature']) + u"\u00B0" + ' F')
                self.feelslike.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.feelslike.setText('Feels like: ' + self.current_weather['FeelsLike'] + u"\u00B0" + ' F')
                self.dewpoint.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.dewpoint.setText('Dew Point: ' + self.current_weather['DewPoint'] + u"\u00B0" + ' F')
                self.humidity.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.humidity.setText('Humidity: ' + self.current_weather['Humidity'])
                self.wind.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.wind.setText('Wind: ' + self.current_weather['Wind'])
                self.chanceofrain.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.chanceofrain.setText(self.current_weather['ChanceofRain'] + ' Chance of Rain')
                self.hightemp.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                if self.hightemp > 80 and self.hightemp < 90:
                    self.image = self.addImage('bikinifrog.jpg')
                elif self.hightemp > 90:
                    self.image = self.addImage('bonefrog')
                elif self.hightemp < 80 and self.hightemp > 70:
                    self.image = self.addImage('sunfrog')
                elif self.hightemp < 70 and self.hightemp > 60:
                    self.image = self.addImage('jacketfrog')
                elif self.hightemp < 60 and self.hightemp > 50:
                    self.image = self.addImage('chillyfrog')
                elif self.hightemp < 50:
                    self.image = self.addImage('frozenfrog')
                self.hightemp.setText("Today's High: " + self.current_weather['HighTemp'] + u"\u00B0" + ' F')
                self.lowtemp.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.lowtemp.setText("Today's Low: " + self.current_weather['LowTemp'] + u"\u00B0" + ' F')
                self.hourlabel1.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour1['summary']) < 8:
                    self.hourlabel1.setText(str(self.hour1['time']) + self.space1 + self.hour1['summary'] + self.space2 + str(self.hour1['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel1.setText(str(self.hour1['time']) + self.space1 + self.hour1['summary'] + self.space1 + str(self.hour1['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour1['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel2.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel2.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel2.setText('\t' + str(self.hour1['rainchance']) + "% Chance of Precipitation")
                self.hourlabel3.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour2['summary']) < 8:
                    self.hourlabel3.setText(str(self.hour2['time']) + self.space1 + self.hour2['summary'] + self.space2 + str(self.hour2['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel3.setText(str(self.hour2['time']) + self.space1 + self.hour2['summary'] + self.space1 + str(self.hour2['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour2['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel4.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel4.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel4.setText('\t' + str(self.hour2['rainchance']) + " % Chance of Precipitation")
                self.hourlabel5.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour3['summary']) < 8:
                    self.hourlabel5.setText(str(self.hour3['time']) + self.space1 + self.hour3['summary'] + self.space2 + str(self.hour3['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel5.setText(str(self.hour3['time']) + self.space1 + self.hour3['summary'] + self.space1 + str(self.hour3['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour3['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel6.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel6.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel6.setText('\t' + str(self.hour3['rainchance']) + " % Chance of Precipitation")
                self.hourlabel7.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour4['summary']) < 8:
                    self.hourlabel7.setText(str(self.hour4['time']) + self.space1 + self.hour4['summary'] + self.space2 + str(self.hour4['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel7.setText(str(self.hour4['time']) + self.space1 + self.hour4['summary'] + self.space1 + str(self.hour4['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour4['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel8.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel8.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel8.setText('\t' + str(self.hour4['rainchance']) + " % Chance of Precipitation")
                self.hourlabel9.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour5['summary']) < 8:
                    self.hourlabel9.setText(str(self.hour5['time']) + self.space1 + self.hour5['summary'] + self.space2 + str(self.hour5['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel9.setText(str(self.hour5['time']) + self.space1 + self.hour5['summary'] + self.space1 + str(self.hour5['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour5['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel10.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel10.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel10.setText('\t' + str(self.hour5['rainchance']) + " % Chance of Precipitation")
                self.hourlabel11.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour6['summary']) < 8:
                    self.hourlabel11.setText(str(self.hour6['time']) + self.space1 + self.hour6['summary'] + self.space2 + str(self.hour6['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel11.setText(str(self.hour6['time']) + self.space1 + self.hour6['summary'] + self.space1 + str(self.hour6['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour6['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel12.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel12.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel12.setText('\t' + str(self.hour6['rainchance']) + " % Chance of Precipitation")
                self.hourlabel13.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour7['summary']) < 8:
                    self.hourlabel13.setText(str(self.hour7['time']) + self.space1 + self.hour7['summary'] + self.space2 + str(self.hour7['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel13.setText(str(self.hour7['time']) + self.space1 + self.hour7['summary'] + self.space1 + str(self.hour7['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour7['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel14.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel14.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel14.setText('\t' + str(self.hour7['rainchance']) + " % Chance of Precipitation")
                self.hourlabel15.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour7['summary']) < 8:
                    self.hourlabel15.setText(str(self.hour8['time']) + self.space1 + self.hour7['summary'] + self.space2 + str(self.hour8['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel15.setText(str(self.hour8['time']) + self.space1 + self.hour7['summary'] + self.space1 + str(self.hour8['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour8['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel16.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel16.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel16.setText('\t' + str(self.hour8['rainchance']) + " % Chance of Precipitation")
                self.hourlabel17.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour9['summary']) < 8:
                    self.hourlabel17.setText(str(self.hour9['time']) + self.space1 + self.hour9['summary'] + self.space2 + str(self.hour9['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel17.setText(str(self.hour9['time']) + self.space1 + self.hour9['summary'] + self.space1 + str(self.hour9['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour9['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel18.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel18.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel18.setText('\t' + str(self.hour9['rainchance']) + " % Chance of Precipitation")
                self.hourlabel19.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour10['summary']) < 8:
                    self.hourlabel19.setText(str(self.hour10['time']) + self.space1 + self.hour10['summary'] + self.space2 + str(self.hour10['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel19.setText(str(self.hour10['time']) + self.space1 + self.hour10['summary'] + self.space1 + str(self.hour10['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour10['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel20.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel20.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel20.setText('\t' + str(self.hour10['rainchance']) + " % Chance of Precipitation")
                self.hourlabel21.setStyleSheet("font-weight:bold; font-family:Purisa; color:yellow")
                self.hourlabel21.setText(str(self.hour11['time']) + '\t\t' + self.hour11['summary'] + '\t\t' + str(self.hour11['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour11['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel22.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel22.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel22.setText('\t' + str(self.hour11['rainchance']) + " % Chance of Precipitation")

            elif self.current_weather['location'] == 'Long Beach':
                self.timelabelLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.timelabelLB.setText(time.strftime("%I:%M %p"))
                self.summaryLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.summaryLB.setText(self.current_weather['Conditions'])
                self.temperatureLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.temperatureLB.setText('Temp: ' + self.current_weather['Temperature'] + u"\u00B0" + ' F')
                self.feelslikeLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.feelslikeLB.setText('Feels like: ' + self.current_weather['FeelsLike'] + u"\u00B0" + ' F')
                self.dewpointLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.dewpointLB.setText('Dew Point: ' + self.current_weather['DewPoint'] + u"\u00B0" + ' F')
                self.humidityLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.humidityLB.setText('Humidity: ' + self.current_weather['Humidity'])
                self.windLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.windLB.setText('Wind: ' + self.current_weather['Wind'])
                self.chanceofrainLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.chanceofrainLB.setText(self.current_weather['ChanceofRain'] + ' Chance of Rain')
                self.hightempLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.hightempLB.setText("Today's High: " + self.current_weather['HighTemp'] + u"\u00B0" + ' F')
                self.lowtempLB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightsteelblue")
                self.lowtempLB.setText("Today's Low: " + self.current_weather['LowTemp'] + u"\u00B0" + ' F')
                self.hourlabel1LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour1['summary']) < 8:
                    self.hourlabel1LB.setText(str(self.hour1['time']) + self.space1 + self.hour1['summary'] + self.space2 + str(self.hour1['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel1LB.setText(str(self.hour1['time']) + self.space1 + self.hour1['summary'] + self.space1 + str(self.hour1['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour1['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel2LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel2LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel2LB.setText('\t' + str(self.hour1['rainchance']) + " % Chance of Precipitation")
                self.hourlabel3LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour2['summary']) < 8:
                    self.hourlabel3LB.setText(str(self.hour2['time']) + self.space1 + self.hour2['summary'] + self.space2 + str(self.hour2['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel3LB.setText(str(self.hour2['time']) + self.space1 + self.hour2['summary'] + self.space1 + str(self.hour2['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour2['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel4LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel4LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel4LB.setText('\t' + str(self.hour2['rainchance']) + " % Chance of Precipitation")
                self.hourlabel5LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour3['summary']) < 8:
                    self.hourlabel5LB.setText(str(self.hour3['time']) + self.space1 + self.hour3['summary'] + self.space2 + str(self.hour3['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel5LB.setText(str(self.hour3['time']) + self.space1 + self.hour3['summary'] + self.space1 + str(self.hour3['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour3['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel6LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel6LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel6LB.setText('\t' + str(self.hour3['rainchance']) + " % Chance of Precipitation")
                self.hourlabel7LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour4['summary']) < 8:
                    self.hourlabel7LB.setText(str(self.hour4['time']) + self.space1 + self.hour4['summary'] + self.space2 + str(self.hour4['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel7LB.setText(str(self.hour4['time']) + self.space1 + self.hour4['summary'] + self.space1 + str(self.hour4['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour4['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel8LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel8LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel8LB.setText('\t' + str(self.hour4['rainchance']) + " % Chance of Precipitation")
                self.hourlabel9LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour5['summary']) < 8:
                    self.hourlabel9LB.setText(str(self.hour5['time']) + self.space1 + self.hour5['summary'] + self.space2 + str(self.hour5['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel9LB.setText(str(self.hour5['time']) + self.space1 + self.hour5['summary'] + self.space1 + str(self.hour5['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour5['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel10LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel10LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel10LB.setText('\t' + str(self.hour5['rainchance']) + " % Chance of Precipitation")
                self.hourlabel11LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour6['summary']) < 8:
                    self.hourlabel11LB.setText(str(self.hour6['time']) + self.space1 + self.hour6['summary'] + self.space2 + str(self.hour6['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel11LB.setText(str(self.hour6['time']) + self.space1 + self.hour6['summary'] + self.space1 + str(self.hour6['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour6['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel12LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel12LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel12LB.setText('\t' + str(self.hour6['rainchance']) + " % Chance of Precipitation")
                self.hourlabel13LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour7['summary']) < 8:
                    self.hourlabel13LB.setText(str(self.hour7['time']) + self.space1 + self.hour7['summary'] + self.space2 + str(self.hour7['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel13LB.setText(str(self.hour7['time']) + self.space1 + self.hour7['summary'] + self.space1 + str(self.hour7['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour7['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel14LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel14LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel14LB.setText('\t' + str(self.hour7['rainchance']) + " % Chance of Precipitation")
                self.hourlabel15LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour8['summary']) < 8:
                    self.hourlabel15LB.setText(str(self.hour8['time']) + self.space1 + self.hour8['summary'] + self.space2 + str(self.hour8['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel15LB.setText(str(self.hour8['time']) + self.space1 + self.hour8['summary'] + self.space1 + str(self.hour8['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour8['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel16LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel16LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel16LB.setText('\t' + str(self.hour8['rainchance']) + " % Chance of Precipitation")
                self.hourlabel17LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                if len(self.hour9['summary']) < 8:
                    self.hourlabel17LB.setText(str(self.hour9['time']) + self.space1 + self.hour9['summary'] + self.space2 + str(self.hour9['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel17LB.setText(str(self.hour9['time']) + self.space1 + self.hour9['summary'] + self.space1 + str(self.hour9['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour9['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel18LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel18LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel18LB.setText('\t' + str(self.hour9['rainchance']) + " % Chance of Precipitation")
                self.hourlabel19LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:lightgoldenrodyellow")
                if len(self.hour10['summary']) < 8:
                    self.hourlabel19LB.setText(str(self.hour10['time']) + self.space1 + self.hour10['summary'] + self.space2 + str(self.hour10['temperature']) + u"\u00B0" + ' F')
                else:
                    self.hourlabel19LB.setText(str(self.hour1['time']) + self.space1 + self.hour10['summary'] + self.space1 + str(self.hour10['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour10['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel20LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel20LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel20LB.setText('\t' + str(self.hour10['rainchance']) + " % Chance of Precipitation")
                self.hourlabel21LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:darkorchid")
                self.hourlabel21LB.setText(str(self.hour11['time']) + '\t\t' + self.hour11['summary'] + '\t\t' + str(self.hour11['temperature']) + u"\u00B0" + ' F')
                num = float(self.hour11['rainchance'] / 2)
                color = colors[int(math.ceil(num))]
                self.hourlabel22LB.setStyleSheet("font-weight:bold; font-family:Purisa; color:{}".format(color))
                self.hourlabel22LB.setAlignment(QtCore.Qt.AlignLeft)
                self.hourlabel22LB.setText('\t' + str(self.hour11['rainchance']) + " % Chance of Precipitation")
            QtGui.QApplication.processEvents()

    def iter_labels(self):
        for i in range(self.layout8.count()):
            item = self.layout8.itemAt(i)
            if type(item) == QtGui.QLayoutItem:
                print(item.layout())
            if type(item) == QtGui.QLabel:
                item.clear()

    def bearing_to_direction(self, bearing):
        directions = ["N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", "NNW"]
        return directions[int((bearing + 15) / 30)]

    def get_weather(self, location, lat, lng):
        weather_list = list()
        req = urllib2.Request(URL + APIKEY + "/" + ("%f,%f" % (lat, lng)))
        response = urllib2.urlopen(req)
        parsed = json.loads(response.read())
        with open(FILE_PATH, "w") as f:
            f.write(json.dumps(parsed, indent=4, sort_keys=True))
        now_dict = collections.OrderedDict()
        current = parsed["currently"]
        daily = parsed["daily"]["data"][0]
        now_time = time.strftime("%I" + ":00" + " %p")
        now_dict['location'] = location
        now_dict['nowtime'] = str(now_time)
        now_dict['Conditions'] = current["summary"]
        now_dict['Temperature'] = str(current["temperature"]).split('.')[0]
        now_dict['FeelsLike'] = str((current["apparentTemperature"])).split('.')[0]
        now_dict['DewPoint'] = ("%.1f" % current["dewPoint"])
        now_dict['Humidity'] = ("%4.1f%%" % (current["humidity"] * 100.))
        now_dict['Wind'] = str(int(round(current["windSpeed"]))) + " mph " + self.bearing_to_direction(current["windBearing"])
        now_dict['ChanceofRain'] = str(int(current["precipProbability"] * 100)) + "%"
        now_dict['HighTemp'] = str((daily["temperatureMax"])).split('.')[0]
        now_dict['LowTemp'] = str((daily["temperatureMin"])).split('.')[0]
        weather_list.append(now_dict)
        hourly = parsed["hourly"]["data"]

        for x in hourly[:12]:
            T = x["temperature"]
            V = x["windSpeed"]
            windchill = math.ceil(35.74 + (0.6215 * T) - (35.75 * (V ** 0.16)) + (0.4275 * T * (V ** 0.16)))
            hour_dict = collections.OrderedDict()
            hour_dict['location'] = location
            hour_dict['time'] = time.strftime('%I %p', time.localtime(x['time']))
            hour_dict['summary'] = x['summary']
            hour_dict['temperature'] = str(x['temperature']).split('.')[0]
            hour_dict['feelslike'] = str(x['apparentTemperature']).split('.')[0]
            hour_dict['dewpoint'] = x['dewPoint']
            hour_dict['humidity'] = int((x['humidity'] * 100))
            hour_dict['rainchance'] = int((x['precipProbability'] * 100))
            hour_dict['windspeed'] = x['windSpeed']
            hour_dict['windchill'] = windchill
            weather_list.append(hour_dict)
        return weather_list


def run():
    app = QtGui.QApplication(sys.argv)
    weather = Weather()
    weather.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    Process.chgProcessName('weathergui')
    APIKEY = "5345c8ecbd9441de62c7b048f21c963d"
    URL = "https://api.forecast.io/forecast/"
    LOCATIONS = {'Lucedale': (30.9252, -88.5900),
                 'Long Beach': (30.3505, -89.1528)}
    FILE_PATH = os.getcwd() + os.sep + "WEATHER.cache"
    run()
