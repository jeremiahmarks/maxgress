#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2016-01-02 21:48:25
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2016-01-03 12:18:21
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt


samplepoints = [[1, 6], [2,8], [2,2], [3,5], [4,7], [4,4], [4,0], [5,6], [5,2], [6,0xa], [6,8], [7,7], [7,6], [7,4], [7,1], [8.6], [8,5], [8,2], [9,4], [9,0], [0xa,9], [0xa,8], [0xa,6], [0xa,2]]


hull1 = ConvexHull(samplepoints)
hullPoints = hull1.vertices

plt.plot(samplepoints)
