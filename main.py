#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:23:28
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-10 16:36:25
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')
from module.sort import * 
from module.operate import *
from module.basic import * 
from module.db import *
from module.config import * 

def load_data():
    bcp_load_apk_basic()
    bcp_load_sm_alarm()
    get_url_details()
    get_virus_sm_detail()

clear_pass()
if sys.argv[1] == 'run':
    print 'begin to run.......'
    load_data()
    report_generator()
else:
    print 'clear done!!!'