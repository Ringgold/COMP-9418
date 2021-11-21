'''
COMP9418 Assignment 2
This file is the example code to show how the assignment will be tested.

Name: Dezhao Chen           zID: z5302273

Name: Ziqiao Ringgold Lin   zID: z5324329
'''

# Make division default to floating-point, saving confusion
from __future__ import division
from __future__ import print_function

# Allowed libraries 
import numpy as np
import pandas as pd
import scipy as sp
import scipy.special
import heapq as pq
import matplotlib as mp
import matplotlib.pyplot as plt
import math
from itertools import product, combinations
from collections import OrderedDict as odict
import collections
from graphviz import Digraph, Graph
from tabulate import tabulate
import copy
import sys
import os
import datetime
import sklearn
import ast
import re
import pickle
import json

###################################
# Code stub
#
# The only requirement of this file is that is must contain a function called get_action,
# and that function must take sensor_data as an argument, and return an actions_dict
#

# th is the threshold, every 15 secs if the number of people above the th, then the light turns on
th = 0.20

# state is the number of people in each space
state = [0] * 40
state.append(20)
state = np.array(state)

# dict room store the relationship between list position in state and the name of the room
room = {}

room_list = [
    'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 
    'r11', 'r12', 'r13', 'r14', 'r15', 'r16', 'r17', 'r18', 'r19', 'r20', 
    'r21', 'r22', 'r23', 'r24', 'r25', 'r26', 'r27', 'r28', 'r29', 'r30', 
    'r31', 'r32', 'r33', 'r34', 'r35', 'c1', 'c2', 'c3', 'c4', 'o1', 'outside'
]

for i in range(len(room_list)):
    room[room_list[i]] = i


tran_matrix_data = pd.read_csv('tran_matrix.csv')
tran_matrix = {'t1': [], 't2': []}

for line in tran_matrix_data:
    if 't1' in line:
        tran_matrix['t1'].append(list(tran_matrix_data[line]))
    elif 't2' in line:
        tran_matrix['t2'].append(list(tran_matrix_data[line]))

for t in tran_matrix.keys():
    tran_matrix[t] = np.array(tran_matrix[t])

def get_action(sensor_data):
    # declare these staff as global so they can be a part of the function
    global state
    global tran_matrix
    global room
    global th

    # multiple the state with transition matrix to get the next state
    # before adjust with sensors and robots
    if int(sensor_data['time'].hour) < 17:
        state = state @ tran_matrix['t1']
    elif int(sensor_data['time'].hour) == 17 and int(sensor_data['time'].minute) < 30:
        state = state @ tran_matrix['t1']
    else:
        state = state @ tran_matrix['t2']

    # adjustment with room sensors
    sensor_list = [["reliable_sensor1", "r16", 0.963, 0.009],
                   ["reliable_sensor2", "r5", 0.706, 0.001],
                   ["reliable_sensor3", "r25", 0.902, 0.014],
                   ["reliable_sensor4", "r31", 0.969, 0.009],
                   ["unreliable_sensor1", "o1", 0.813, 0.018],
                   ["unreliable_sensor2", "c3", 0.716, 0.035],
                   ["unreliable_sensor3", "r1", 0.786, 0.016],
                   ["unreliable_sensor4", "r24", 0.354, 0.003],
                   ]

    for slist in sensor_list:
        if sensor_data[slist[0]] == "motion" and state[room[slist[1]]] < th:
            state[room[slist[1]]] = slist[2]
        if sensor_data[slist[0]] == "no motion" and state[room[slist[1]]] > th:
            state[room[slist[1]]] = slist[3]

    # adjustment with door sensors
    door_list = [["door_sensor1", "r8", "r9", 0.390, 0.609],
                 ["door_sensor2", "c1", "c2", 0.940, 0.703],
                 ["door_sensor3", "r26", "r27", 0.514, 0.649],
                 ["door_sensor4", "r35", "c4", 0.566, 0.977],
                 ]
    for dlist in door_list:
        if sensor_data[dlist[0]] and int(sensor_data[dlist[0]]) > 0:
            if state[room[dlist[1]]] < th:
                state[room[dlist[1]]] = dlist[3]
            if state[room[dlist[2]]] < th:
                state[room[dlist[2]]] = dlist[4]

    # robot
    for r in ['robot1', 'robot2']:
        if sensor_data[r]:
            position = sensor_data[r].split(',')[0].strip('(').strip("'")
            people = sensor_data[r].split(',')[1].strip(')')
            state[room[position]] = int(people)

    # generate the actions based on states
    # if the number of people in a room is more than the threshold
    # then turn on the light
    actions_dict = {}

    for r in range(0, 35):
        light = "lights" + str(r+1)
        if state[r] > th:
            actions_dict[light] = 'on'
        else:
            actions_dict[light] = 'off'

    return actions_dict
