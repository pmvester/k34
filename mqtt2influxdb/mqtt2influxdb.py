# -*- coding: utf-8 -*-

import json
import paho.mqtt.client as mqtt
import time
from influxdb import InfluxDBClient

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("k34/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic)
    #print(str(msg.payload))
    try:
      pl = json.loads(msg.payload)
      if msg.topic == "k34/bmp085":
        json_body = [
          {
            "measurement": "pressure",
            "time": pl["time"] * 1000000,
            "fields": {
              "pressure": pl["pressure"],
              "temperature": pl["temperature"]
            }
          }
        ]
        db.write_points(json_body)
      elif msg.topic == "k34/heat/water":
        json_body = [
          {
            "measurement": "heatWater",
            "time": pl["timestamp"] * 1000000,
            "fields": {
              "feedTemp": pl["temperature"]["feed"],
              "returnTemp": pl["temperature"]["return"]
            }
          }
        ]
        db.write_points(json_body)
      elif msg.topic == "k34/power":
        json_body = [
          {
            "measurement": "power",
            "time": pl["timestamp"] * 1000000,
            "fields": {
              "power": pl["power"]
            }
          }
        ]
        db.write_points(json_body)
      elif msg.topic == "k34/tempout":
        json_body = [
          {
            "measurement": "tempout",
            "time": long(time.time() * 1000000000),
            "fields": {
              "tempout": pl["temperature"]
            }
          }
        ]
        db.write_points(json_body)
      elif msg.topic == "k34/tempgarage":
        json_body = [
          {
            "measurement": "tempgarage",
            "time": long(time.time() * 1000000000),
            "fields": {
              "tempout": pl["temperature"]
            }
          }
        ]
        db.write_points(json_body)
      elif msg.topic == "k34/heat/burner":
        json_body = [
          {
            "measurement": "oilBurner",
            "time": pl["timestamp"] * 1000000,
            "fields": {
              "burner": pl["burner"]
            }
          }
        ]
        db.write_points(json_body)
      else:
        pass
    except:
      print("something went wrong, probably unintelligible payload")

db = InfluxDBClient("localhost", 8086, "root", "root", "k34db")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_forever()
