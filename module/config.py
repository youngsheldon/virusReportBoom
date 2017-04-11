#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:22:31
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-11 11:59:37
import time 
import datetime 

def get_setting():
    dict_set = {}
    f = open('conf/setting.conf')
    for line in f:
        v = line.strip().split('=')
        if len(v) > 1:
            dict_set[v[0]] = v[1]
    f.close()
    return dict_set 
    
def city_map():
    city_dict = {}
    f = open('conf/setting.conf') 
    for line in f:
        v = line.strip().split(',')
	if len(v) == 3:
        	city_dict[v[2]] = [v[0] + v[1],v[0]]
    f.close()
    return city_dict

def get_yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    date = str(yesterday).split('-')
    return date[0] + date[1] + date[2]

def get_today():
    today = datetime.date.today()
    date = str(today).split('-')
    return date[0] + date[1] + date[2]

dict_set = get_setting()
city_dict = city_map()
today = get_today()
yesterday = get_yesterday()