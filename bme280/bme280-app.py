import bme280
import smbus2
import apscheduler
import sys
import time
import paho.mqtt.publish as publish

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from datetime import timedelta

port = 1
address = 0x77
bus = smbus2.SMBus(port)

bme280.load_calibration_params(bus, address)

def publishData():
  d = bme280.sample(bus, address)
  json = '{"pressure": %f, "humidity": %f, "temperature": %f, "time": %d}' % (d.pressure, d.humidity, d.temperature, int(time.time())*1000)
  try:
    publish.single("k34/bme280", json, hostname="k34.mine.nu")
  except:
    pass

try:
  sched = BackgroundScheduler()
  sched.start()

  sched.add_job(publishData, 'cron', minute='*/1')

  while(True):
    time.sleep(3600.0)
except KeyboardInterrupt:
  pass
