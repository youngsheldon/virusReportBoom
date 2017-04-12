#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:31:22
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-12 09:27:57
from basic import *
from config import * 
import commands
import os

def get_url_c():
    url_dict = {}
    ip_dict = get_ip_map()
    url_ip_dict = get_url_map()
    virus_sm_path = dict_set['VirusDir']
    v_url_list = get_virusUrl()
    for url in v_url_list:
        cmd = 'grep ' + url + ' ' + virus_sm_path + ' | wc -l'
        v_c = cmd_exec(cmd)
        if url_ip_dict.has_key(url):
            ip = url_ip_dict[url]
        else:
            ip = 'unknow'
        if ip_dict.has_key(ip):
            ip_bl = ip_dict[ip]
        else:
            ip_bl = 'unknow'
        url_dict[url] = (v_c,ip,ip_bl)
    return url_dict 

def get_url_details():
    date_list = set_date()
    for date in date_list:
        cmd = 'cp ' + dict_set['SourceDir'] + date + ' ' + dict_set['TarDir']
        os.system(cmd)

def get_virus_sm_detail():
    urls = get_virusUrl()
    for url in urls: 
        cmd = 'grep ' + url + ' ' + dict_set['TarDir'] + '*' + ' >> ' + dict_set['VirusDir']
        os.system(cmd)

def get_phone_num_belong():
    cmd1 = 'cat ' + dict_set['VirusDir'] + ' | awk -F' '\',\' \'{print $10}\' | grep 2 | wc -l'
    cmd2 = 'cat ' + dict_set['VirusDir'] + ' | awk -F' '\',\' \'{print $10}\' | grep 9 | wc -l'
    cmd3 = 'cat ' + dict_set['VirusDir'] + ' | awk -F' '\',\' \'{print $10}\' | grep 10 | wc -l'
    ret1 = commands.getstatusoutput(cmd1)
    ret2 = commands.getstatusoutput(cmd2)
    ret3 = commands.getstatusoutput(cmd3)
    return ret1[1],ret2[1],ret3[1] 

def get_timeinterval_count():
    rets = []
    for hour in range(0,24):
        if hour < 10:
            hour = '0' + str(hour)
        else:
            hour = str(hour)
        cmd = 'cat ' + dict_set['VirusDir'] + '* | awk -F \',\' \'{print $8}\' | cut -c12-13 | grep ' + hour +    ' | wc -l' 
        ret = commands.getstatusoutput(cmd)
        rets.append(int(ret[1]))
    return rets 

def get_virus_sm_src_c():
    cmd = 'cat ' + dict_set['VirusDir'] + ' | awk -F \',\' \'{print $9}\' | sort | uniq | wc -l'
    return cmd_exec(cmd)

def get_v_src_top6():
    cmd = 'cat ' + dict_set['VirusDir'] + ' | awk -F \',\' \'{print $9}\' | cut -c1-4 | sort | uniq -c | sort -k1nr -k2 | head -6 | awk -F \' \' \'{print $2}\''
    return cmd_exec(cmd)

def provin_take(state,bl,st,ed):
    if state == 'in':
        cmd = 'cat ' + dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | awk -F \' \' \'{if($2>=' + st + ' && $2<=' + ed + ')print $2}\' |wc -l'
    else:
        cmd = 'cat ' + dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | awk -F \' \' \'{if($2<' + st + ' || $2>' + ed + ')print $2}\' |wc -l'
    return cmd 

def gd_provin_take(state,bl):
    if state == 'in':
        cmd = 'cat ' + dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | ' + 'awk -F \' \' \'{if($2==20 || ($2>=660&&$2<=668) || ($2>=750&&$2<=769))print $2}\'' + ' | wc -l'
    else:
        cmd = 'cat ' + dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | ' + 'awk -F \' \' \'{if($2!=20 && ($2<660||$2>668) && ($2<750||$2>769))print $2}\'' + ' | wc -l'
    return cmd 

def get_provin_proportion():
    gd_state = dict_set['GdSet']
    if gd_state == 'ON':
        cmd_tele_in = gd_provin_take('in',2)
        cmd_tele_out = gd_provin_take('out',2)
        cmd_mobi_in = gd_provin_take('in',9,)
        cmd_mobi_out = gd_provin_take('out',9)
        cmd_uni_in = gd_provin_take('in',10)
        cmd_uni_out = gd_provin_take('out',10)
    else:
        st = dict_set['ProvinSt']
        ed = dict_set['ProvinEd']
        cmd_tele_in = provin_take('in',2,st,ed)
        cmd_tele_out = provin_take('out',2,st,ed)
        cmd_mobi_in = provin_take('in',9,st,ed)
        cmd_mobi_out = provin_take('out',9,st,ed)
        cmd_uni_in = provin_take('in',10,st,ed)
        cmd_uni_out = provin_take('out',10,st,ed)
    cmds =[cmd_tele_in,cmd_tele_out,cmd_mobi_in,cmd_mobi_out,cmd_uni_in,cmd_uni_out]
    return cmd_exec(cmds)
    