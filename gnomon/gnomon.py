# -*- coding: utf-8 -*-

import datetime
import logging
import time
import paho.mqtt.publish as publish

from apscheduler.schedulers.blocking import BlockingScheduler
from astral import Astral

logging.basicConfig()

k34lat = 59.313254
k34lon = 18.188412

a = Astral()
a.solar_depression = 'civil'

def logData():
  now = time.time()
  dt = datetime.datetime.fromtimestamp(now, tz=None)
  azimuth = a.solar_azimuth(dt, k34lat, k34lon)
  elevation = a.solar_elevation(dt, k34lat, k34lon)
  json = '{"azimuth": %f, "elevation": %f, "timestamp": %d}' % (azimuth, elevation, int(now * 1000))
  try:
    publish.single("k34/gnomon", payload=json, hostname="k34.mine.nu")
  except:
    pass

scheduler = BlockingScheduler()
scheduler.add_job(logData, 'cron', minute='*/1')
scheduler.start()
