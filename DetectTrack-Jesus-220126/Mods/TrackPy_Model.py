'''
 # @ Author: J.N. Hayek
 # @ Create Time: 2022-01-29 14:57:26
 # @ Modified by: J.N. Hayek
 # @ Modified time: 2022-01-29 22:46:59
 # @ Description: Some functions to clean up the V4 of the tracking script
 '''

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

import matplotlib as mpl
import matplotlib.pyplot as plt


import numpy as np
import pandas as pd

import trackpy as tp
import trackpy.predict

#
def detectFilter(frame):
    f = tp.locate(frame, 11, invert=False, maxsize=2)
    return f

@trackpy.predict.predictor
def predict(t1, particle):
    velocity = np.array((150, 0))
    return particle.pos + velocity * (t1 - particle.t)