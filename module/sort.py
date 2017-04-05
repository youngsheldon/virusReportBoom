#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:40:54
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-05 18:02:16
from operate import * 
from config import * 
from basic import *

type_dict = {1:'�����г�������ջ����Ķ����漰�ƻ���ͥ�����ݣ����״̼��û�����������ӣ�������ಡ�����Ӻ���Զ�ת���������Ÿ�ͨѶ¼�����ϵ�ˣ���Ⱦ�����ֻ��û����γ�ɢ��ʽ������ʽ������ȡ�ֻ��ϵ�ȫ����Ϣ�������û����ֻ��ϵ�¼�����п��˺ż�������Ͷ���Ϣ���������ز������������ţ���������ת�ơ�Ⱥ�����ŵȣ����ʺš��ʽ����������в��',2:'�����г�������ջ����Ķ����漰�ƻ���ͥ�����ݣ����״̼��û�����������ӣ�������ಡ�����Ӻ���Զ�ת���������Ÿ�ͨѶ¼�����ϵ�ˣ���Ⱦ�����ֻ��û����γ�ɢ��ʽ������ʽ������ȡ�ֻ��ϵ�ȫ����Ϣ�������û����ֻ��ϵ�¼�����п��˺ż�������Ͷ���Ϣ���������ز������������ţ���������ת�ơ�Ⱥ�����ŵȣ����ʺš��ʽ����������в��',3:'����թƭ��Ҫͨ��ģ��УѶͨ��ð���ʦ��ѧ���ҳ����͸�����У������ϡ��˷ѡ�����ѧϰ�࣬ѧ��ͻ��������ҽ�ȷ�ʽ���ܺ���ʵʩթƭ��ͨ����ȡ�ֻ�ͨѶ¼�����ز�ת���ţ���ȡ�ֻ�֧����֤�룬��ˢ�ֻ������ʽ�',4:'����թƭ��Ҫͨ��ģ����������򱻽з��ͻ��硢�������ϲ������ȷ�ʽ���ܺ���ʵʩթƭ��ͨ����ȡ�ֻ�ͨѶ¼�����ز�ת���ţ���ȡ�ֻ�֧����֤�룬��ˢ�ֻ������ʽ�',5:'�û�����ò�����ַ�󣬻ᱻ���ز�ת�����ţ���ȡ���ż�¼���ֻ�ͨ��¼�ȸ����û�������Ϣ',6:'����'}
virus_type = {1:'��Ƶ',2:'���',3:'УѶͨ',4:'ϲ������',5:'�ʼ���',6:'����'}

def virus_source_search():
    #������Դ
    provin_list = []
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

def src_sum():
    #�������Ű�����ȥ������
    v_sms_src_c = get_virus_sm_src_c()
    print 'v_sms_src_c=' + str(v_sms_src_c) 
    out = '�������Ű�����ȥ������' + '\n'
    out += str(v_sms_src_c) + '\n\n'
    w2f(out)

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