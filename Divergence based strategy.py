# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 19:11:25 2022

@author: Sam
"""

#Creating a divergence based strategy
#we need to rollingwindows

closewindow = rollingwindow(50)[float]
rsiwindow = rollingwindow(50)[indicatordatapoint]

