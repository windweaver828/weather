#!/usr/bin/env python2


import forecastio
import datetime


APIKEY = "5345c8ecbd9441de62c7b048f21c963d"

LOCATIONS = {'Lucedale': (30.9252, -88.5900),
             'Long Beach': (30.3505, -89.1528)}


if __name__ == "__main__":
    for location, x in LOCATIONS.items():
        latitude, longitude = x
        forecast = forecastio.load_forecast(APIKEY, latitude, longitude, units='us')
        hourly_weather = forecast.hourly()
        print
        print(location)
        print(hourly_weather.summary)
        max_hours = 12
        cur_hour = datetime.datetime.now().hour
        loop_hour = 0
        skipped = False
        for data in hourly_weather.data:
            if data.time.hour < cur_hour and not skipped:
                continue
            if loop_hour >= max_hours:
                break
            skipped = True
            time = data.time.strftime('%I:%M %p')
            print("{} - {}F - {}".format(time, int(data.temperature), data.summary))
            precip = data.precipProbability
            print("{}% chance of rain".format(int(precip * 100)))
            loop_hour += 1
