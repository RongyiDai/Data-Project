#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 11:16:02 2019

@author: dairongyi
"""

import time
import datetime
import numpy as np
import pandas as pd
import selenium
from selenium import webdriver
import sys
import os
import io
import re
import matplotlib.pyplot as plt

imdb250_df = pd.read_csv('imdb250.csv')
imdb250_df = imdb250_df.replace('-', np.NaN)
year = imdb250_df['year']
year_count = year.value_counts()
pd.to_numeric(imdb250_df['meta'])
try:
    imdb250_df.meta = imdb250_df.meta / 10
except:
    pass

plt.bar(year_count.index, year_count)
plt.xlabel('Year')
plt.ylabel('Number of Films')
plt.show()

plt.figure()
plt.xticks(())
plt.plot(imdb250_df.name, imdb250_df.rating, color = 'red')
plt.plot(imdb250_df.name, imdb250_df.meta)
plt.show()