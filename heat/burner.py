# -*- coding: utf-8 -*-

import logging
import paho.mqtt.publish as publish
import numpy as np
import time

from adxl345 import ADXL345
from apscheduler.schedulers.background import BackgroundScheduler
  
class AggregatedState:

  def __init__(self):
    self.threeState = False
    self.state = [False, False, False]
    self.timestamp = int(time.time() * 1000)

  def getState(self):
    return self.threeState

  def setState(self, s):
    self.state[2] = self.state[1]
    self.state[1] = self.state[0]
    self.state[0] = s
    allTrue = self.state[0] and self.state[1] and self.state[2]
    allFalse = not (self.state[0] or self.state[1] or self.state[2])
    if allTrue and not self.threeState:
      self.timestamp = int(time.time() * 1000)
      self.threeState = True
    elif allFalse and self.threeState:
      self.timestamp = int(time.time() * 1000)
      self.threeState = False

class ADXL:

  def __init__(self):
    self.adxl345 = ADXL345()
    self.y = np.zeros(2000)
    self.sampleCount = 0

  def sample1s(self):
    self.sampleCount = 0
    t_end = time.time() + 1.0
    while time.time() < t_end:
      axes = self.adxl345.getAxes(True)
      self.y[self.sampleCount] = axes['y']
      self.sampleCount += 1
  
  def measure(self):
    self.sample1s()
    
    yd = np.array(self.y[0:self.sampleCount-1])
    yn = np.fft.fft(yd)
    
    freq = np.fft.fftfreq(self.sampleCount, 1.0 / self.sampleCount)
    ind = np.arange(1, self.sampleCount / 2)
    
    self.ypsd = abs(yn[ind]) ** 2 + abs(yn[-ind]) ** 2
    self.yf = freq[ind[np.where(self.ypsd >= max(self.ypsd))]]
    self.ypsdm = max(self.ypsd)
    #print "%.2f, %.2f" % (self.ypsdm, self.yf)

  def getState(self):
    return (self.yf[0] > 50) and (self.yf[0] < 70) and (self.ypsdm > 100)
    
def publishData(timestamp, state):
  json = '{"timestamp": %d, "burner": %i}' % (timestamp, state)
  try:
    publish.single("k34/heat/burner", payload=json, hostname="k34.mine.nu")
    #print json
  except:
    pass

updateFlag = True

def setFlag():
  global updateFlag
  updateFlag = True

burner = AggregatedState()
adxl = ADXL()

logging.basicConfig()
scheduler = BackgroundScheduler()
scheduler.add_job(setFlag, 'cron', minute='*/1', misfire_grace_time=30)
scheduler.start()

while True:
  previousState = burner.getState()
  adxl.measure()
  burner.setState(adxl.getState())
  newState = burner.getState()
  if newState != previousState:
    publishData(burner.timestamp, newState)
  elif updateFlag:
    publishData(time.time() * 1000, newState)
    updateFlag = False
