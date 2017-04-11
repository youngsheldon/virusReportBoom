#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:40:54
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-11 19:14:46
from operate import * 
from config import * 
from basic import *

type_dict = {1:'该类有冲击力和诱惑力的短信涉及破坏家庭的内容，容易刺激用户点击病毒链接，点击该类病毒链接后会自动转发病毒短信给通讯录里的联系人，感染其它手机用户，形成散发式传播方式。可窃取手机上的全部信息，包括用户在手机上登录的银行卡账号及其密码和短信息，还可拦截并屏蔽正常短信，开启呼叫转移、群发短信等，对帐号、资金造成严重威胁。',2:'该类有冲击力和诱惑力的短信涉及破坏家庭的内容，容易刺激用户点击病毒链接，点击该类病毒链接后会自动转发病毒短信给通讯录里的联系人，感染其它手机用户，形成散发式传播方式。可窃取手机上的全部信息，包括用户在手机上登录的银行卡账号及其密码和短信息，还可拦截并屏蔽正常短信，开启呼叫转移、群发短信等，对帐号、资金造成严重威胁。',3:'此类诈骗主要通过模仿校讯通或冒充教师向学生家长发送个人在校情况资料、退费、开办学习班，学生突发疾病就医等方式向受害人实施诈骗，通过窃取手机通讯录，拦截并转短信，窃取手机支付验证码，盗刷手机银行资金。',4:'此类诈骗主要通过模仿亲朋好友向被叫发送婚宴、生日宴等喜宴邀请等方式向受害人实施诈骗，通过窃取手机通讯录，拦截并转短信，窃取手机支付验证码，盗刷手机银行资金。',5:'用户点击该病毒网址后，会被拦截并转发短信，窃取短信记录、手机通信录等各种用户个人信息',6:'待定'}
virus_type = {1:'视频',2:'相册',3:'校讯通',4:'喜宴请帖',5:'邮件类',6:'待定'}

def virus_source_search():
    #病毒溯源
    provin_list = []
    victim_dict = {}
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
            victim_dict[url] = vs 
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
    return victim_dict

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
    return url_like_sm_c,virus_sm_c,virus_sm_reject_c

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
    return t_dev_list

def src_sum():
    #病毒短信按主叫去重总数
    v_sms_src_c = get_virus_sm_src_c()
    print 'v_sms_src_c=' + str(v_sms_src_c) 
    out = '病毒短信按主叫去重总数' + '\n'
    out += str(v_sms_src_c) + '\n\n'
    w2f(out)
    return v_sms_src_c

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
    return vs 

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
    return provin_take_list 

def virus_type_sort():
    cmd = 'cat ' + dict_set['VirusDir'] + ' | grep -E \'视频|录相|录像|视屏\'' + ' | wc -l' 
    cmd2 = 'cat ' + dict_set['VirusDir'] + ' | grep -vE \'视频|录相|录像|视屏\'' +  ' | grep -E \'看|瞧|瞅\'' + ' | wc -l'
    cmd3 = 'cat ' + dict_set['VirusDir'] + ' | wc -l'
    video_type = int(exec_shell_scrip(cmd))
    photo_type = int(exec_shell_scrip(cmd2))
    all_type = int(exec_shell_scrip(cmd3))
    other_type = all_type - video_type - photo_type 
    v_t = float(1.0 * video_type/all_type)
    p_t = float(1.0 * photo_type/all_type)
    o_t = float(1.0 * other_type/all_type)
    out = '各类病毒短信占比情况' + '\n'
    out += '视频类,' + '相册类,' + '其它类,' + '\n' 
    out += str(video_type) + ',' + str(photo_type) + ',' + str(other_type) + '\n'
    out += str(v_t) + ',' + str(p_t) + ',' + str(o_t) + '\n\n'
    w2f(out)
    return video_type,photo_type,other_type


def virus_case_detail(tar,type):
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
    return v_type,p_type,o_type

def apk_belong():
    url_dict = get_url_c()
    out = 'URL' + ',' + '发送量' + ',' + 'IP' + ',' + 'IP归属地' + '\n'
    for k,v in url_dict.items():
        out += k + ',' + v[0] + ',' + v[1] + ',' + v[2] + '\n'
    path = dict_set['ResultFile'] + 'ip_bl_' + time_section + '.csv'
    f = open(path,'a+')
    f.write(out)
    f.close()
    return url_dict

def summarize():
    url_like_count, virus_sum_count, reject_sum_count = overall_profile()
    vl = provin_sent()
    tele_in_count = vl[0]
    tele_out_count = vl[1]
    mobile_in_count = vl[2]
    mobile_out_count = vl[3]
    union_in_count = vl[4]
    union_out_count = vl[5]
    src_uniq_count = src_sum()
    video_type_count, album_type_count, other_type_count = virus_type_sort()
    sql = 'insert into virus_report_summarize(date_time,url_like_count,virus_sum_count,reject_sum_count,tele_in_count,tele_out_count,mobile_in_count,mobile_out_count,union_in_count,union_out_count,src_uniq_count,video_type_count,album_type_count,other_type_count) values(to_date(' + '\'' + get_datetime() + '\'' + ',\'YYYY-MM-DD\')' + ',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d);' % (url_like_count,virus_sum_count,reject_sum_count,tele_in_count,tele_out_count,mobile_in_count,mobile_out_count,union_in_count,union_out_count,src_uniq_count,video_type_count,album_type_count,other_type_count)
    sql_exec(sql)

def virus_period_send():
    tl = timeinterval_send()
    sql = 'insert into virus_period_send(date_time,t0_c,t1_c,t2_c,t3_c,t4_c,t5_c,t6_c,t7_c,t8_c,t9_c,t10_c,t11_c,t12_c,t13_c,t14_c,t15_c,t16_c,t17_c,t18_c,t19_c,t20_c,t21_c,t22_c,t23_c) values (to_date(' + '\'' + get_datetime() + '\'' + ',\'YYYY-MM-DD\')' +',%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d);' % (tl[0],tl[1],tl[2],tl[3],tl[4],tl[5],tl[6],tl[7],tl[8],tl[9],tl[10],tl[11],tl[12],tl[13],tl[14],tl[15],tl[16],tl[17],tl[18],tl[19],tl[20],tl[21],tl[22],tl[23])
    sql_exec(sql)

def src_segment_top6():
    vl = phonenum_top6()
    sql = 'insert into src_segment_top6(date_time,\'seg0\',\'seg1\',\'seg2\',\'seg3\',\'seg4\',\'seg5\') values(to_date(' + '\'' + get_datetime() + '\'' + ',\'YYYY-MM-DD\')' + ',%s,%s,%s,%s,%s,%s);' % (vl[0],vl[1],vl[2],vl[3],vl[4],vl[5])
    sql_exec(sql)

def virus_type_insert(t_list):
    sql = 'insert into virus_type_example(date_time,type,url,sm_text,ip,ip_attribution) values(to_date(' +  '\'' + get_datetime() + '\'' + ',\'YYYY-MM-DD\')' + ',%d,\'%s\',\'%s\',\'%s\',\'%s\');' % (int(t_list[0]),t_list[1],t_list[2],t_list[4],t_list[5])
    sql_exec(sql)

def virus_type_example():
    v_l, v_p,o_l = case_show()
    virus_type_insert(v_l)
    virus_type_insert(v_p)
    virus_type_insert(o_l)

def url_ip_relate():
    url_dict = apk_belong()
    for k,v in url_dict.items():
        if int(v[0]) > 0:
            sql = 'insert into url_ip_relate(date_time,url,send_count,ip,ip_attribution) values(to_date' + '\'' + get_datetime() + '\'' + ',\'YYYY-MM-DD\')' + ',\'%s\',%d,\'%s\',\'%s\');' % (k,int(v[0]),v[1],v[2])
            sql_exec(sql)
    
def victim_distribution():
    victim_dict = virus_source_search()
    for url,city_list in victim_dict.items():
        for city in city_list:
            sql = 'call sp_vir_victim_distribution(\'%s\',\'%s\');' % (url,city)
            sql_exec(sql)

def virus_source_sqls(path):
    sql_list = []
    with open(path,'r') as f:
        for line in f:
            v = line.strip().split(',')
            id = v[0].split(':')[1]
            urlGrade = v[1]
            urlCode = v[2]
            url = v[3]
            nti_code = v[4]
            msgid = v[5]
            smcid = v[6]
            recv_time = v[7]
            src = v[8]
            src_type = v[9]
            src_locate = v[10]
            dst = v[11]
            dst_type = v[12]
            dst_locate = v[13]
            state = v[14]
            alarm_type = v[15]
            alarm_resp = v[16]
            hash = v[17]
            nosymbol = v[18]
            content = v[19]
            sql = 'call sp_vir_source_rec(\'%s\',%d,\'%s\',\'%s\',\'%s\',\'%s\',%d,%s,\'%s\',%d,%d,\'%s\',%d,%d,\'%s\',%d,\'%s\',\'%s\',\'%s\',\'%s\');' % (id,int(urlGrade),urlCode,url,nti_code,msgid,int(smcid),'to_date(\'' + recv_time + '\',\'YYYY-MM-DD HH24:MI:SS\')',src,int(src_type),int(src_locate),dst,int(dst_type),int(dst_locate),state,int(alarm_type),alarm_resp,hash,nosymbol,content)
            sql_list.append(sql)
    return sql_list

def update_virus_source():
    path = dict_set['ResultFile'] + 'virus_source_' + time_section + '.csv' 
    sql_list = virus_source_sqls(path)
    sql_exec(sql_list)

def report_generator():
    summarize()
    virus_period_send()
    src_segment_top6()
    virus_type_example()
    url_ip_relate()
    victim_distribution()
    update_virus_source()