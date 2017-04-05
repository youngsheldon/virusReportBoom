#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:22:31
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-05 17:19:42

def get_setting():
    dict_set = {}
    f = open('../conf/setting.conf')
    for line in f:
        v = line.strip().split('=')
        if len(v) > 1:
            dict_set[v[0]] = v[1]
    f.close()
    return dict_set 
    
def city_map():
    city_dict = {}
    f = open('../conf/setting.conf','r') 
    for line in f:
        v = line.strip().split(',')
        city_dict[v[2]] = [v[0] + v[1],v[0]]
    f.close()
    return city_dict

dict_set = get_setting()
city_dict = city_map()