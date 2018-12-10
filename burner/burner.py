# -*- coding: utf-8 -*-

import smbus
import time

TSLaddr = 0x39 #Default I2C address, alternate 0x29, 0x49 
TSLcmd = 0x80 #Command
chan0 = 0x0C #Read Channel0 sensor date
chan1 = 0x0E #Read channel1 sensor data
TSLon = 0x03 #Switch sensors on
TSLoff = 0x00 #Switch sensors off

#Exposure settings
LowShort = 0x00 #x1 Gain 13.7 miliseconds
LowMed = 0x01 #x1 Gain 101 miliseconds
LowLong = 0x02 #x1 Gain 402 miliseconds
LowManual = 0x03 #x1 Gain Manual
HighShort = 0x10 #LowLight x16 Gain 13.7 miliseconds
HighMed = 0x11  #LowLight x16 Gain 100 miliseconds
HighLong = 0x12 #LowLight x16 Gain 402 miliseconds
HighManual = 0x13 #LowLight x16 Gain Manual

def createTimestamp():
  return int(time.time() * 1000)

class Burner:
  def __init__(self):
    self.ch0 = 0
    self.ch1 = 0
    self.timestamp = createTimestamp()
    self.bus = smbus.SMBus(1)
    self.writebyte = self.bus.write_byte_data

    self.writebyte(TSLaddr, 0x00 | TSLcmd, TSLon)

  def __del__(self):
    self.writebyte(TSLaddr, 0x00 | TSLcmd, TSLoff)

  def measure(self):
    self.writebyte(TSLaddr, 0x01 | TSLcmd, HighLong)
    self.timestamp = createTimestamp()
    time.sleep(1.0)

    data = self.bus.read_i2c_block_data(TSLaddr, chan0 | TSLcmd, 2)
    data1 = self.bus.read_i2c_block_data(TSLaddr, chan1 | TSLcmd, 2)
    self.ch0 = data[1] * 256 + data[0]
    self.ch1 = data1[1] * 256 + data1[0]

  def getCh0(self):
    return self.ch0

  def getCh1(self):
    return self.ch1

  def getState(self):
    return (self.ch0 > 5) and (self.ch1 > 5)
