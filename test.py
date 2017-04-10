#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-10 16:16:50
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-10 16:29:42
import datetime 

def get_yesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=12)
    date = str(yesterday).split('-')
    return date[0] + date[1] + date[2]

print get_yesterday()