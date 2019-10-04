#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#coding=utf-8
"""
Created on Fri Mar 29 17:39:17 2019

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

options = webdriver.ChromeOptions()
options.set_headless()
#sys.stdout = io.TextIOWrapper(buffer=sys.stdout.buffer, encoding='utf-8') #sys.stdout.buffer

class IMDb250():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/Users/dairongyi/Desktop/Python Project/chromedriver') #options = options
        chromedriver_path = '/Users/dairongyi/Desktop/Python Project/chromedriver'
        os.path.exists(chromedriver_path) 
        self.base_url = 'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
    
        
    def get_info(self): 
        self.driver.get(self.base_url)
        time.sleep(3)
        count = 1
        page_num = 5

        df_tot = pd.DataFrame()
        
        while count <= page_num:
            print(count)
            film_list = []
            body = self.driver.find_elements_by_xpath('//*[@id="main"]/div/div[3]/div/div')
#                                                      //*[@id="main"]/div/div[3]/div
            for i in range(0, len(body)):
                film_content = body[i].find_element_by_class_name('lister-item-content')
    #            film_header = col_body[i].find_element_by_class_name('lister-item-header')
                
                index = film_content.find_element_by_xpath('h3/span[1]').text[:-1]
                name = film_content.find_element_by_xpath('h3/a').text
                year = int(''.join(re.findall(r"[0-9]", film_content.find_element_by_xpath('h3/span[2]').text)))
                certi = film_content.find_element_by_xpath('p[1]/span[1]').text
                genre = film_content.find_element_by_class_name('genre').text
                rating = film_content.find_element_by_xpath('div/div[1]').text
                try:
                    meta = film_content.find_element_by_xpath('div/div[3]/span[1]').text
                except:
                    meta = '-'
                director = film_content.find_element_by_xpath('p[3]/a[1]').text
                try:
                    boxoff = film_content.find_element_by_xpath('p[4]/span[5]').text
                except:
                    boxoff = '-'
                film = [index, name, year, certi, genre, rating, meta, director, boxoff]
                
                print(film)
                film_list.append(film)
            
            column_name = ['index', 'name', 'year', 'certi', 'genre', 'rating', 'meta', 'director', 'boxoff']
            df = pd.DataFrame(film_list, columns = column_name)
            df_tot = pd.concat([df_tot, df], axis = 0)
            df_tot = df_tot.reset_index(drop = True)
            
            if count == 1:
                self.driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/a').click()
                count += 1
                time.sleep(7)
            else:
                try:
                    self.driver.find_element_by_xpath('//*[@id="main"]/div/div[4]/a[2]').click()
                    count += 1
                    time.sleep(7)
                except:
                    count += 1
                    pass
        df_tot.to_csv('imdb250.csv', encoding = 'utf_8_sig')
        return df_tot
        
            
            
if __name__ == '__main__':
    self = IMDb250()
#    date_start = '2019-06-05'
#    latest_date = '2019-06-10'
#    oldest_date = '2019-06-06'
    self.get_info()
#    print ('Sum')
#    print (result)
    
    self.driver.quit()