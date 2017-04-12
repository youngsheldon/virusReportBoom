#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:26:36
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-12 18:15:06
import commands 
import time 
import datetime 
from config import * 

mode = dict_set['RunMode']
if mode == 'DAY':
    virus_alarm_path = dict_set['RefDir'] + 'virus_sm_alarm_' + yesterday[0:6] + '.csv'
    time_section = yesterday[0:8]
else:
    st = dict_set['DateStart']
    virus_alarm_path = dict_set['RefDir'] + 'virus_sm_alarm_' + st[0:6] + '.csv'
    time_section = dict_set['DateStart'] + '_' +dict_set['DateEnd'][6:]

apk_basic_info_path = dict_set['RefDir'] + 'apk_basic_info.csv'

def get_virus_apk_md5():
    v_apk_md5_list = []
    f = open(apk_basic_info_path,'r')
    for line in f:
        v = line.strip().split(',')
        virus_flag = int(v[12])
        md5 = v[2]
        if virus_flag > 1:
            v_apk_md5_list.append(md5)
    f.close()
    return v_apk_md5_list 

def get_ip_map():
    ip_dict = {}
    f = open(apk_basic_info_path,'r')
    for line in f:
        v = line.strip().split(',')
        ip_tar1 = v[16]
        ip_tar_belong1 = v[17]
        ip_dict[ip_tar1] = ip_tar_belong1
        ip_tar2 = v[18]
        ip_tar_belong2 = v[19]
        ip_dict[ip_tar2] = ip_tar_belong2
    f.close()
    return ip_dict 

def get_virus_sm_list():
    virus_sm_list = []
    v_apk_md5_list = get_virus_apk_md5()
    f = open(virus_alarm_path,'r')
    for line in f:
        v = line.strip().split(',')
        md5 = v[12]
        if md5 in v_apk_md5_list:
            virus_sm_list.append(v)
    f.close()
    return virus_sm_list 

def get_virusUrl():
    url_list = []
    virus_sm_list = get_virus_sm_list()
    for v in virus_sm_list:
        url_list.append(v[7])
    return list(set(url_list))

def get_url_map():
    url_ip_dict = {}
    f = open(virus_alarm_path,'r')
    for line in f:
        v = line.strip().split(',')
        url = v[7]
        ip = v[11]
        url_ip_dict[url] = ip 
    f.close()
    return url_ip_dict

def set_date():
    mode = dict_set['RunMode']
    date_list = []
    if mode == 'DAY':
        yesterday = get_yesterday()
        v = 'url_detail_' + yesterday + '*'
        date_list.append(v)
    else:
        st = dict_set['DateStart']
        ed = dict_set['DateEnd']
        st_v = int(st[6]) * 10 + int(st[7])
        ed_v = int(ed[6]) * 10 + int(ed[7])
        for index in range(st_v,ed_v):
            if index < 10:
                v = 'url_detail_' + st[0:6] + '0' + str(index) + '*'
                date_list.append(v)
            else:
                v = 'url_detail_' + st[0:6] + str(index) + '*'
                date_list.append(v)
        if ed_v < 10:
            v = 'url_detail_' + st[0:6] + '0' + str(ed_v) + '*'
            date_list.append(v)
        else:
            v = 'url_detail_' + st[0:6] + str(ed_v) + '*'
            date_list.append(v)
    return date_list 

def get_count(path):
    cmd = 'cat ' + path + ' | wc -l'
    ret = commands.getstatusoutput(cmd)
    return ret[1]

def cmd_exec(cmd):
    ret_list = []
    if isinstance(cmd,list):
        for v in cmd:
            ret = commands.getstatusoutput(v)
            ret_list.append(ret[1])
        return ret_list 
    else:
        ret = commands.getstatusoutput(cmd)
        return ret[1]

def w2f(content):
    path = dict_set['ResultFile'] + 'ret_' + time_section + '.csv'
    if isinstance(content,list):
        f = open(path,'a+')
        out = ''
        for v in content:
            out += v + ','
        out += '\n'
        f.write(out)
        f.close()
    else:
        f = open(path,'a+')
        f.write(content)
        f.close()

def w2f2(path,content):
    f = open(path,'a+')
    f.write(content)
    f.close()

def get_sm_alarm_tbname():
    st = dict_set['DateStart']
    tb_n = 'virus_sm_alarm_' + st[0:6]
    return tb_n

def rm_blank_lines(path):
    cmd = 'sed -i \'/^$/d\' ' + path 
    cmd_exec(cmd)

def exec_shell_scrip(cmd):
    f = open('cmd.sh','w+')
    f.write(cmd)
    f.close()
    ret = cmd_exec('bash cmd.sh')
    cmd_exec('rm cmd.sh')
    return ret 
    
def clear_pass():
    cmd = 'rm ' + dict_set['TarDir'] + '* ' + dict_set['RefDir'] + '* ' + dict_set['VirusDir'] 
    cmd_exec(cmd)

def get_datetime():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return str(yesterday)

def divi(num1,num2):
    if num1 == 0 or num2 == 0:
        return 0 
    else:
        return float(1.0*num1/num1 + num2)