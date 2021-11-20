import numpy as np
import pandas as pd

data = pd.read_csv('data.csv')
#print(data,len(data))

# ob = {}
# calculate TP,FN
# true positive, false negative

def room_sensor(sensor, room):
    motion = data[sensor].value_counts()["motion"]
    nomotion = data[sensor].value_counts()["no motion"]
    tp = ((data[sensor] == "motion") & (data[room] != 0)).value_counts()[True]
    fn = ((data[sensor] == "no motion") & (data[room] != 0)).value_counts()[True]
    print('TP for', sensor, ':', tp / motion)
    print('FN for', sensor, ':', fn / nomotion)
    print()


def door_sensor(sensor, room1, room2):
    tp1, fn1 = 0, 0
    tp2, fn2 = 0, 0
    nopassed = data[sensor].value_counts()[0]
    passed = len(data[sensor]) - nopassed
    tp1 = ((data[sensor] != 0) & (data[room1] != 0)).value_counts()[True]
    fn1 = ((data[sensor] == 0) & (data[room1] != 0)).value_counts()[True]
    tp2 = ((data[sensor] != 0) & (data[room2] != 0)).value_counts()[True]
    fn2 = ((data[sensor] == 0) & (data[room2] != 0)).value_counts()[True]
    print('TP for', sensor, 'of', room1, ':', tp1 / passed)
    print('FN for', sensor, 'of', room1, ':', fn1 / nopassed)
    print('TP for', sensor, 'of', room2, ':', tp2 / passed)
    print('FN for', sensor, 'of', room2, ':', fn2 / nopassed)
    print(passed, nopassed)
    print()

room_sensor("reliable_sensor1", "r16")
room_sensor("reliable_sensor2", "r5")
room_sensor("reliable_sensor3", "r25")
room_sensor("reliable_sensor4", "r31")
room_sensor("unreliable_sensor1", "o1")
room_sensor("unreliable_sensor2", "c3")
room_sensor("unreliable_sensor3", "r1")
room_sensor("unreliable_sensor4", "r24")

door_sensor('door_sensor1','r8','r9')
door_sensor('door_sensor2','c1','c2')
door_sensor('door_sensor3','r26','r27')
door_sensor('door_sensor4','r35','c4')



