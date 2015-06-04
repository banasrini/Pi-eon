# -*- coding: utf-8 -*-
import os
import time
import sys
from Pubnub import Pubnub

pubnub = Pubnub(publish_key='demo', subscribe_key='demo')
channel = 'tempeon'

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-000006b4fef4/w1_slave'

def callback(message):
    print(message)

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0 
        pubnub.publish('tempeon', {
            'message': {
                'columns': [
                    ['x', time.time()],
                    ['temp', temp_c],
                    ['tempf', temp_f]
                    ]
                }
            })
        return temp_c, temp_f

while True:
    print(read_temp())
    time.sleep(1)
