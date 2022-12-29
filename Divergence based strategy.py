# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 19:11:25 2022

@author: Sam
"""

#Creating a divergence based strategy
#we need to rollingwindows

closewindow = rollingwindow(50)[float]
rsiwindow = rollingwindow(50)[indicatordatapoint]

#Sifting through data to identify hills and valleys from the data on the rolling windows

#Our expected output should yield the most recent either 
#2 hills; ch1, ch2 or 2 valleys; cv1, cv2
##2 hills; rh1, rh2 or 2 valleys; rv1, rv2

#We will check first if a divergence is forming or a convergence is forming instead
# Checking for Divergence
# Asuming we know our hills and valleys
#What datapoints will we use
divergence1 = ch1 < ch2 and rv1 > rv2
divergence2 = cv1 < cv2 and rh1 > rh2
#is there a scenario where divergence can happen when hills of both the price and
#rsi diverge or valleys of both price and rsi diverge

#When the divergence is noticed make sure you log the time and date to cross check on an
#actual chart.

