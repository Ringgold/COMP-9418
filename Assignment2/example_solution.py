'''
COMP9418 Assignment 2
This file is the example code to show how the assignment will be tested.
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
from get_trans_matrix import outcomeSpace

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

# index_r is the dictionary storing each room and its corresponding index of state, and index_l is
# the dictionary storing each light and its corresponding index of state.
index_r = {}
index_l = {}
start = 0
for key in outcomeSpace.keys():
    index_r[key] = start
    if start < 35:
        index_l['lights' + str(start + 1)] = start
    start += 1

params = pd.read_csv('tran_matrix.csv')
# train_matrix stores five time period of markov transition matrix.
tran_matrix = {}
tran_matrix['s1'] = []
# tran_matrix['s2'] = []
# tran_matrix['s3'] = []

for r in params:
    if r[-2:] == 's1':
        tran_matrix['s1'].append(list(params[r]))
    # elif r[-2:] == 's2':
    #     tran_matrix['s2'].append(list(params[r]))
    # elif r[-2:] == 's3':
    #     tran_matrix['s3'].append(list(params[r]))

for l in tran_matrix.keys():
    tran_matrix[l] = np.array(tran_matrix[l])


def get_action(sensor_data):
    # declare state as a global variable so it can be read and modified within this function
    global state
    global tran_matrix
    global index_r
    global index_l
    global th

    state = state @ tran_matrix['s1']
    # different time use different transition matrix
    # if int(sensor_data['time'].hour) == 8 and int(sensor_data['time'].minute) < 5:
    #     state = state @ tran_matrix['s1']
    # elif int(sensor_data['time'].hour) < 17:
    #     state = state @ tran_matrix['s2']
    # elif int(sensor_data['time'].hour) == 17 and int(sensor_data['time'].minute) < 30:
    #     state = state @ tran_matrix['s2']
    # else:
    #     state = state @ tran_matrix['s3']

    # adjustment for values of reliable sensors
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
        if sensor_data[slist[0]] == "motion" and state[index_r[slist[1]]] < th:
            state[index_r[slist[1]]] = slist[2]
        if sensor_data[slist[0]] == "no motion" and state[index_r[slist[1]]] > th:
            state[index_r[slist[1]]] = slist[3]

    door_list = [["door_sensor1", "r8", "r9", 0.390, 0.609],
                 ["door_sensor2", "c1", "c2", 0.940, 0.703],
                 ["door_sensor3", "r26", "r27", 0.514, 0.649],
                 ["door_sensor4", "r35", "c4", 0.566, 0.977],
                 ]
    for dlist in door_list:
        if sensor_data[dlist[0]] and int(sensor_data[dlist[0]]) > 0:
            if state[index_r[dlist[1]]] < th:
                state[index_r[dlist[1]]] = dlist[3]
            if state[index_r[dlist[2]]] < th:
                state[index_r[dlist[2]]] = dlist[4]

    # robot sensors
    for r in ['robot1', 'robot2']:
        if sensor_data[r]:
            room = sensor_data[r].split(',')[0].strip('(').strip("'")
            people = sensor_data[r].split(',')[1].strip(')')
            state[index_r[room]] = int(people)

    actions_dict = {}
    for key in index_l:
        if state[index_l[key]] > th:
            actions_dict[key] = 'on'
        else:
            actions_dict[key] = 'off'
    
    return actions_dict
