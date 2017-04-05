#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:40:54
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-05 17:37:57
from operate import * 
from config import * 
from basic import *

def virus_source_search():
    #病毒溯源
    provin_list = []
    out = '病毒溯源' + '\n'
    path = dict_set['ResultFile'] + 'victim_' + time_section + '.csv'
    v_url_list = get_virusUrl()
    for url in v_url_list:
        cmd = 'grep ' + url + ' ' + dict_set['VirusDir'] + ' -m 1 >> ' + dict_set['ResultFile'] + 'virus_source_' + time_section + '.csv'
        cmd_exec(cmd)
        cmd = 'grep ' + url + ' ' + dict_set['VirusDir'] + '| awk -F \',\' \'{print $14}\'| sort | uniq '
        city_num_list = cmd_exec(cmd)
        vs = city_num_list.strip().split('\n')
        if len(vs) > 0:
            out += url + ','
            for v in vs:
                if city_dict.has_key(v):
                    out += city_dict[v][0] + ','
                else:
                    out += v + ','
            out += '|'
            for v in vs:
                if city_dict.has_key(v):
                    pro_v = city_dict[v][1]
                else:
                    pro_v = v
                provin_list.append(pro_v)
            provin_list = list(set(provin_list))
            for v in provin_list:
                out += v + ','
            out += '\n'
        provin_list = []
    w2f2(path,out)

def overall_profile():
    #总体概括
    url_like_sm_c = get_count(dict_set['TarDir'] + '*')
    print 'url_like_sm_c=' + str(url_like_sm_c)
    virus_sm_c = get_count(dict_set['VirusDir'])
    print 'virus_sm_c=' + virus_sm_c
    virus_sm_reject_c = get_count(dict_set['VirusDir'] + ' | grep REJECT ')
    print 'virus_sm_reject_c=' + str(virus_sm_reject_c)
    out = '总体概括' + '\n'
    out += '带有网址或网址形态的短信总量,' + '病毒短信总量,' + '可拦截量' + '\n'
    out += str(url_like_sm_c) +',' +str(virus_sm_c) + ','+ str(virus_sm_reject_c) + '\n\n'
    w2f(out)

def operator_distribution():
    #病毒短信各运营商分布
    telecom,mobile,unicom = get_phone_num_belong()
    print 'telecom=' + str(telecom)
    print 'mobile=' + str(mobile)
    print 'unicom=' + str(unicom)
    out = '病毒短信各运营商分布' + '\n'
    out += '电信' + ',' + '移动' + ',' + '联通' + '\n'
    out += str(telecom) + ',' + str(mobile) + ',' + str(unicom) + '\n\n'
    w2f(out)

def timeinterval_send():
    #各时间段病毒短信发送量分布
    t_dev_list = get_timeinterval_count()        
    print 'timeinterval'
    print t_dev_list 
    out = '各时间段病毒短信发送量分布' + '\n'
    for i in range(0,24):
        out += str(i) + ','
    out += '\n'
    for v in t_dev_list:
        out += v + ','
    out += '\n\n'
    w2f(out)

def src_sum():
    #病毒短信按主叫去重总数
    v_sms_src_c = get_virus_sm_src_c()
    print 'v_sms_src_c=' + str(v_sms_src_c) 
    out = '病毒短信按主叫去重总数' + '\n'
    out += str(v_sms_src_c) + '\n\n'
    w2f(out)

def phonenum_top6():
    #病毒短信前6号段
    nub_list = get_v_src_top6()
    print 'nub_list'
    print nub_list 
    out = '病毒短信前6号段' + '\n'
    vs = nub_list.strip().split('\n')
    for v in vs:
        out += v + ','
    out += '\n\n'
    w2f(out)

def provin_sent():
    #各运营商病毒短信省内外发送量占比
    provin_take_list = get_provin_proportion()
    print 'provin_take_list'
    print provin_take_list 
    out = '各运营商病毒短信省内外发送量占比' + '\n'
    out += '电信省内,' + '电信省外,' + '移动省内,' + '移动省外,' + '联通省内,' + '联通省外,' + '\n'
    for v in provin_take_list:
        out += str(v) + ','
    out += '\n'
    pl = []
    for v in provin_take_list:
        pl.append(int(v))
    v1 = str(float(1.0*pl[0]/(pl[0] + pl[1]))) + ','
    v2 = str(float(1.0*pl[1]/(pl[0] + pl[1]))) + ','
    v3 = str(float(1.0*pl[2]/(pl[2] + pl[3]))) + ','
    v4 = str(float(1.0*pl[3]/(pl[2] + pl[3]))) + ','
    v5 = str(float(1.0*pl[4]/(pl[4] + pl[5]))) + ','
    v6 = str(float(1.0*pl[5]/(pl[4] + pl[5]))) + '\n'
    out += v1 + v2 + v3 + v4 + v5 + v6 + '\n'
    w2f(out)

def virus_type_sort():
    cmd = 'cat ' + dict_set['VirusDir'] + ' | grep -E \'视频|录相|录像|视屏\'' + ' | wc -l' 
    cmd2 = 'cat ' + dict_set['VirusDir'] + ' | grep -vE \'视频|录相|录像|视屏\'' +  ' | grep -E \'看|瞧|瞅\'' + ' | wc -l'
    cmd3 = 'cat ' + dict_set['VirusDir'] + ' | wc -l'
    video_type = int(.exec_shell_scrip(cmd))
    photo_type = int(.exec_shell_scrip(cmd2))
    all_type = int(.exec_shell_scrip(cmd3))
    other_type = all_type - video_type - photo_type 
    v_t = float(1.0 * video_type/all_type)
    p_t = float(1.0 * photo_type/all_type)
    o_t = float(1.0 * other_type/all_type)
    out = '各类病毒短信占比情况' + '\n'
    out += '视频类,' + '相册类,' + '其它类,' + '\n' 
    out += str(video_type) + ',' + str(photo_type) + ',' + str(other_type) + '\n'
    out += str(v_t) + ',' + str(p_t) + ',' + str(o_t) + '\n\n'
    w2f(out)

def virus_case_detail(,tar,type):
    ip_dict = get_ip_map()
    cmd ='cat ' + dict_set['VirusDir'] + ' | ' + tar + ' | tail -1 | awk -F \',\' \'{print $4}\''
    url = cmd_exec(cmd)
    cmd ='cat ' + dict_set['VirusDir'] + ' | ' + tar + ' | tail -1 | awk -F \',\' \'{print $19}\''
    sms = cmd_exec(cmd) + url 
    sm_alarm_path = dict_set['RefDir'] + 'virus_sm_alarm_' + dict_set['DateStart'][0:6] + '.csv'
    cmd = 'cat ' + sm_alarm_path + ' | grep ' + url + ' | awk -F \',\' \'{print $12}\' | tail -1'
    ip = cmd_exec(cmd)
    if ip_dict.has_key(ip):
        ip_bl = ip_dict[ip]
    else:
        ip_bl = 'unknow'
    return [virus_type[type],url,sms,type_dict[type],ip,ip_bl]

def case_show():
    v_cmd = 'grep -E \'视频|录相|录像|视屏\''
    v_type = virus_case_detail(v_cmd,2)
    p_cmd = 'grep -vE \'视频|录相|录像|视屏\'' +  ' | grep -E \'看|瞧|瞅\''
    p_type = virus_case_detail(p_cmd,1)
    o_cmd = 'grep -vE \'视频|录相|录像|视屏|看|瞧|瞅\''
    o_type = virus_case_detail(o_cmd,6)
    out = '病毒类型' + ',' + '病毒链接' + ',' + '病毒短信示例' + '恶意行为描述' + ',' + 'IP地址' + ',' + 'IP归属地' + '\n'
    w2f(out)
    w2f(v_type)
    w2f(p_type)
    w2f(o_type)