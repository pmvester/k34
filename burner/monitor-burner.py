# -*- coding: utf-8 -*-

import apscheduler
import logging
import paho.mqtt.publish as publish
import smbus
import time

from apscheduler.schedulers.background import BackgroundScheduler
from burner import Burner

updateFlag = True

def setFlag():
  global updateFlag
  updateFlag = True

def createTimestamp():
  return int(time.time() * 1000)

def publishData(timestamp, state):
  json = '{"timestamp": %d, "burner": %i}' % (timestamp, state)
  try:
    publish.single('k34/heat/burner', payload=json, hostname='k34.mine.nu')
  except:
    pass

burner = Burner()

logging.basicConfig()
scheduler = BackgroundScheduler()
scheduler.add_job(setFlag, 'cron', minute='*/1', misfire_grace_time=30)
scheduler.start()

while True:
  try:
    previousState = burner.getState()
    burner.measure()
    newState = burner.getState()
    if newState != previousState:
      publishData(burner.timestamp, newState)
      updateFlag = False
    elif updateFlag:
      publishData(createTimestamp(), newState)
      updateFlag = False
  except:
    console.log('exception caught')
    pass
