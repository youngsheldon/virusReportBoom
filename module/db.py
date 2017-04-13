#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-04-05 16:13:52
# @Last Modified by:   anchen
# @Last Modified time: 2017-04-13 14:50:29
import os 
from basic import *
from config import * 

def sql_exec(sql):
    sql_exe = ''
    mode = dict_set['RunMode']
    if isinstance(sql,list):
        for v in sql:
            sql_exe += v + '\n'
        out = 'sqlplus smmcadmin/AdminDB^12@SMMC <<!\n' + sql_exe + 'exit;\n' + '!\n'
    else:
        out = 'sqlplus smmcadmin/AdminDB^12@SMMC <<!\n' + sql + '\n' + 'exit;\n' + '!\n'
    if mode == 'DAY':
        os.system(out)

def bcp_load_apk_basic():
    db_version = dict_set['DatabaseVersion']
    if db_version == 'Oracle':
        cmd = 'bash shell/download_apk_basic_info.sh'
        cmd_exec(cmd)
    else:
        pw = dict_set['DatabasePWD']
        s_n = dict_set['DatabaseServer']
        db_n = dict_set['ApkBasicDbName']
        u_n = dict_set['DatabaseUser']
        tb_n = 'apk_basic_info'
        out_p = dict_set['RefDir'] + 'apk_basic_info.csv'
        cmd = 'bcp ' + db_n + '..' + tb_n + ' out ' + out_p + ' -U' + u_n + ' -P' + pw + ' -S' + s_n + ' -c -t\',\' -r\'\\n\''
        cmd_exec(cmd)
    rm_blank_lines(apk_basic_info_path)

def bcp_load_sm_alarm():
    mode = dict_set['RunMode']
    if mode == 'DAY':
        today = get_today()
        date = today[0:6]
    else:
        date = dict_set['DateStart'][0:6]
    db_version = dict_set['DatabaseVersion']
    if db_version == 'Oracle':
        cmd = 'bash shell/download_virus_sm_alarm.sh ' + date 
        cmd_exec(cmd)
    else:
        pw = dict_set['DatabasePWD']
        s_n = dict_set['DatabaseServer']
        db_n = dict_set['SmAlarmDbName']
        u_n = dict_set['DatabaseUser']
        tb_n = get_sm_alarm_tbname()
        out_p = dict_set['RefDir'] + tb_n + '.csv'
        cmd = 'bcp ' + db_n + '..' + tb_n + ' out ' + out_p + ' -U' + u_n + ' -P' + pw + ' -S' + s_n + ' -c -t\',\' -r\'\\n\''
        cmd_exec(cmd)
    rm_blank_lines(virus_alarm_path)