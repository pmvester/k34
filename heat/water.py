# -*- coding: utf-8 -*-

import os
import glob
import paho.mqtt.client as mqtt
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

t = glob.glob('/sys/bus/w1/devices/28*/w1_slave')
tr = t[0]
tf = t[1]

def read_temp_raw(rf):
  f = open(rf, 'r')
  lines = f.readlines()
  f.close()
  return lines

def read_temp(rf):
  lines = read_temp_raw(rf)
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw(rf)
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    return temp_c

mqttc = mqtt.Client()

mqttc.connect("k34.mine.nu", 1883, 60)

while True:
  json = '{"temperature": {"feed": %f, "return": %f}}' % (read_temp(tf), read_temp(tr))
  mqttc.publish("k34/heat/water", payload=json)
  time.sleep(5)

mqttc.loop_forever()
