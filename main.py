#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:23:28
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-05 17:44:59
import sys 
from module.sort import * 
from module.operate import *
from module.basic import * 

def load_data():
    bcp_load_apk_basic()
    bcp_load_sm_alarm()
    get_url_details()
    get_virus_sm_detail()

def run():
    overall_profile()
    operator_distribution()
    timeinterval_send()
    src_sum()
    phonenum_top6()
    virus_type_sort()
    provin_sent()
    apk_belong()
    case_show()
    virus_source_search()

clear_pass()
if sys.argv[1] == 'run':
    print 'begin to run.......'
    load_data()
    run()
else:
    print 'clear done!!!'
clear_pass()