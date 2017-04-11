#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:40:54
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-11 19:14:46
from operate import * 
from config import * 
from basic import *

type_dict = {1:'�����г�������ջ����Ķ����漰�ƻ���ͥ�����ݣ����״̼��û�����������ӣ�������ಡ�����Ӻ���Զ�ת���������Ÿ�ͨѶ¼�����ϵ�ˣ���Ⱦ�����ֻ��û����γ�ɢ��ʽ������ʽ������ȡ�ֻ��ϵ�ȫ����Ϣ�������û����ֻ��ϵ�¼�����п��˺ż�������Ͷ���Ϣ���������ز������������ţ���������ת�ơ�Ⱥ�����ŵȣ����ʺš��ʽ����������в��',2:'�����г�������ջ����Ķ����漰�ƻ���ͥ�����ݣ����״̼��û�����������ӣ�������ಡ�����Ӻ���Զ�ת���������Ÿ�ͨѶ¼�����ϵ�ˣ���Ⱦ�����ֻ��û����γ�ɢ��ʽ������ʽ������ȡ�ֻ��ϵ�ȫ����Ϣ�������û����ֻ��ϵ�¼�����п��˺ż�������Ͷ���Ϣ���������ز������������ţ���������ת�ơ�Ⱥ�����ŵȣ����ʺš��ʽ����������в��',3:'����թƭ��Ҫͨ��ģ��УѶͨ��ð���ʦ��ѧ���ҳ����͸�����У������ϡ��˷ѡ�����ѧϰ�࣬ѧ��ͻ��������ҽ�ȷ�ʽ���ܺ���ʵʩթƭ��ͨ����ȡ�ֻ�ͨѶ¼�����ز�ת���ţ���ȡ�ֻ�֧����֤�룬��ˢ�ֻ������ʽ�',4:'����թƭ��Ҫͨ��ģ����������򱻽з��ͻ��硢�������ϲ������ȷ�ʽ���ܺ���ʵʩթƭ��ͨ����ȡ�ֻ�ͨѶ¼�����ز�ת���ţ���ȡ�ֻ�֧����֤�룬��ˢ�ֻ������ʽ�',5:'�û�����ò�����ַ�󣬻ᱻ���ز�ת�����ţ���ȡ���ż�¼���ֻ�ͨ��¼�ȸ����û�������Ϣ',6:'����'}
virus_type = {1:'��Ƶ',2:'���',3:'УѶͨ',4:'ϲ������',5:'�ʼ���',6:'����'}

def virus_source_search():
    #������Դ
    provin_list = []
    victim_dict = {}
    out = '������Դ' + '\n'
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
    #�������
    url_like_sm_c = get_count(dict_set['TarDir'] + '*')
    print 'url_like_sm_c=' + str(url_like_sm_c)
    virus_sm_c = get_count(dict_set['VirusDir'])
    print 'virus_sm_c=' + virus_sm_c
    virus_sm_reject_c = get_count(dict_set['VirusDir'] + ' | grep REJECT ')
    print 'virus_sm_reject_c=' + str(virus_sm_reject_c)
    out = '�������' + '\n'
    out += '������ַ����ַ��̬�Ķ�������,' + '������������,' + '��������' + '\n'
    out += str(url_like_sm_c) +',' +str(virus_sm_c) + ','+ str(virus_sm_reject_c) + '\n\n'
    w2f(out)
    return url_like_sm_c,virus_sm_c,virus_sm_reject_c

def operator_distribution():
    #�������Ÿ���Ӫ�̷ֲ�
    telecom,mobile,unicom = get_phone_num_belong()
    print 'telecom=' + str(telecom)
    print 'mobile=' + str(mobile)
    print 'unicom=' + str(unicom)
    out = '�������Ÿ���Ӫ�̷ֲ�' + '\n'
    out += '����' + ',' + '�ƶ�' + ',' + '��ͨ' + '\n'
    out += str(telecom) + ',' + str(mobile) + ',' + str(unicom) + '\n\n'
    w2f(out)

def timeinterval_send():
    #��ʱ��β������ŷ������ֲ�
    t_dev_list = get_timeinterval_count()        
    print 'timeinterval'
    print t_dev_list 
    out = '��ʱ��β������ŷ������ֲ�' + '\n'
    for i in range(0,24):
        out += str(i) + ','
    out += '\n'
    for v in t_dev_list:
        out += v + ','
    out += '\n\n'
    w2f(out)
    return t_dev_list

def src_sum():
    #�������Ű�����ȥ������
    v_sms_src_c = get_virus_sm_src_c()
    print 'v_sms_src_c=' + str(v_sms_src_c) 
    out = '�������Ű�����ȥ������' + '\n'
    out += str(v_sms_src_c) + '\n\n'
    w2f(out)
    return v_sms_src_c

def phonenum_top6():
    #��������ǰ6�Ŷ�
    nub_list = get_v_src_top6()
    print 'nub_list'
    print nub_list 
    out = '��������ǰ6�Ŷ�' + '\n'
    vs = nub_list.strip().split('\n')
    for v in vs:
        out += v + ','
    out += '\n\n'
    w2f(out)
    return vs 

def provin_sent():
    #����Ӫ�̲�������ʡ���ⷢ����ռ��
    provin_take_list = get_provin_proportion()
    print 'provin_take_list'
    print provin_take_list 
    out = '����Ӫ�̲�������ʡ���ⷢ����ռ��' + '\n'
    out += '����ʡ��,' + '����ʡ��,' + '�ƶ�ʡ��,' + '�ƶ�ʡ��,' + '��ͨʡ��,' + '��ͨʡ��,' + '\n'
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
    cmd = 'cat ' + dict_set['VirusDir'] + ' | grep -E \'��Ƶ|¼��|¼��|����\'' + ' | wc -l' 
    cmd2 = 'cat ' + dict_set['VirusDir'] + ' | grep -vE \'��Ƶ|¼��|¼��|����\'' +  ' | grep -E \'��|��|��\'' + ' | wc -l'
    cmd3 = 'cat ' + dict_set['VirusDir'] + ' | wc -l'
    video_type = int(exec_shell_scrip(cmd))
    photo_type = int(exec_shell_scrip(cmd2))
    all_type = int(exec_shell_scrip(cmd3))
    other_type = all_type - video_type - photo_type 
    v_t = float(1.0 * video_type/all_type)
    p_t = float(1.0 * photo_type/all_type)
    o_t = float(1.0 * other_type/all_type)
    out = '���ಡ������ռ�����' + '\n'
    out += '��Ƶ��,' + '�����,' + '������,' + '\n' 
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
    v_cmd = 'grep -E \'��Ƶ|¼��|¼��|����\''
    v_type = virus_case_detail(v_cmd,2)
    p_cmd = 'grep -vE \'��Ƶ|¼��|¼��|����\'' +  ' | grep -E \'��|��|��\''
    p_type = virus_case_detail(p_cmd,1)
    o_cmd = 'grep -vE \'��Ƶ|¼��|¼��|����|��|��|��\''
    o_type = virus_case_detail(o_cmd,6)
    out = '��������' + ',' + '��������' + ',' + '��������ʾ��' + '������Ϊ����' + ',' + 'IP��ַ' + ',' + 'IP������' + '\n'
    w2f(out)
    w2f(v_type)
    w2f(p_type)
    w2f(o_type)
    return v_type,p_type,o_type

def apk_belong():
    url_dict = get_url_c()
    out = 'URL' + ',' + '������' + ',' + 'IP' + ',' + 'IP������' + '\n'
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