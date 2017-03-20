#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2017-03-02 09:53:22
# @Last Modified by:   anchen
# @Last Modified time: 2017-03-20 11:30:02
import os 
import commands 
import sys
import time
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

type_dict = {1:'该类有冲击力和诱惑力的短信涉及破坏家庭的内容，容易刺激用户点击病毒链接，点击该类病毒链接后会自动转发病毒短信给通讯录里的联系人，感染其它手机用户，形成散发式传播方式。可窃取手机上的全部信息，包括用户在手机上登录的银行卡账号及其密码和短信息，还可拦截并屏蔽正常短信，开启呼叫转移、群发短信等，对帐号、资金造成严重威胁。',2:'该类有冲击力和诱惑力的短信涉及破坏家庭的内容，容易刺激用户点击病毒链接，点击该类病毒链接后会自动转发病毒短信给通讯录里的联系人，感染其它手机用户，形成散发式传播方式。可窃取手机上的全部信息，包括用户在手机上登录的银行卡账号及其密码和短信息，还可拦截并屏蔽正常短信，开启呼叫转移、群发短信等，对帐号、资金造成严重威胁。',3:'此类诈骗主要通过模仿校讯通或冒充教师向学生家长发送个人在校情况资料、退费、开办学习班，学生突发疾病就医等方式向受害人实施诈骗，通过窃取手机通讯录，拦截并转短信，窃取手机支付验证码，盗刷手机银行资金。',4:'此类诈骗主要通过模仿亲朋好友向被叫发送婚宴、生日宴等喜宴邀请等方式向受害人实施诈骗，通过窃取手机通讯录，拦截并转短信，窃取手机支付验证码，盗刷手机银行资金。',5:'用户点击该病毒网址后，会被拦截并转发短信，窃取短信记录、手机通信录等各种用户个人信息',6:'待定'}
virus_type = {1:'视频',2:'相册',3:'校讯通',4:'喜宴请帖',5:'邮件类',6:'待定'}

class Statistics(object):
    def __init__(self):
        self.dict_set = self.get_setting()
        self.apk_basic_info_path = self.dict_set['RefDir'] + 'apk_basic_info.csv'
        st = self.dict_set['DateStart']
        self.virus_alarm_path = self.dict_set['RefDir'] + 'virus_sm_alarm_' + st[0:6] + '.csv'
    
    def get_virus_apk_md5(self):
        v_apk_md5_list = []
        f = open(self.apk_basic_info_path,'r')
        for line in f:
            v = line.strip().split(',')
            virus_flag = int(v[12])
            md5 = v[2]
            if virus_flag > 1:
                v_apk_md5_list.append(md5)
        f.close()
        return v_apk_md5_list 

    def get_ip_map(self):
        ip_dict = {}
        f = open(self.apk_basic_info_path,'r')
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

    def get_virus_sm_list(self):
        virus_sm_list = []
        v_apk_md5_list = self.get_virus_apk_md5()
        f = open(self.virus_alarm_path,'r')
        for line in f:
            v = line.strip().split(',')
            md5 = v[12]
            if md5 in v_apk_md5_list:
                virus_sm_list.append(v)
        f.close()
        return virus_sm_list 

    def get_virusUrl(self):
        url_list = []
        virus_sm_list = self.get_virus_sm_list()
        for v in virus_sm_list:
            url_list.append(v[7])
        return list(set(url_list))

    def get_url_map(self):
        url_ip_dict = {}
        f = open(self.virus_alarm_path,'r')
        for line in f:
            v = line.strip().split(',')
            url = v[7]
            ip = v[11]
            url_ip_dict[url] = ip 
        f.close()
        return url_ip_dict

    def get_url_c(self):
        url_dict = {}
        ip_dict = self.get_ip_map()
        url_ip_dict = self.get_url_map()
        virus_sm_path = self.dict_set['VirusDir']
        v_url_list = self.get_virusUrl()
        for url in v_url_list:
            cmd = 'grep ' + url + ' ' + virus_sm_path + ' | wc -l'
            v_c = self.cmd_exec(cmd)
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

    def apk_belong(self):
        url_dict = self.get_url_c()
        out = 'URL' + ',' + '发送量' + ',' + 'IP' + ',' + 'IP归属地' + '\n'
        for k,v in url_dict.items():
            out += k + ',' + v[0] + ',' + v[1] + ',' + v[2] + '\n'
        path = self.dict_set['ResultFile'] + 'ip_bl.csv'
        f = open(path,'a+')
        f.write(out)
        f.close()

    def set_date(self):
        date_list = []
        st = self.dict_set['DateStart']
        ed = self.dict_set['DateEnd']
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

    def get_url_details(self):
        date_list = self.set_date()
        for date in date_list:
            cmd = 'cp ' + self.dict_set['SourceDir'] + date + ' ' + self.dict_set['TarDir']
            os.system(cmd)

    def get_virus_sm_detail(self):
        urls = self.get_virusUrl()
        for url in urls: 
            cmd = 'grep ' + url + ' ' + self.dict_set['TarDir'] + '*' + ' >> ' + self.dict_set['VirusDir'] 
            os.system(cmd)

    def get_count(self,path):
        cmd = 'cat ' + path + ' | wc -l'
        ret = commands.getstatusoutput(cmd)
        return ret[1]

    def get_phone_num_belong(self):
        cmd1 = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F' '\',\' \'{print $10}\' | grep 2 | wc -l'
        cmd2 = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F' '\',\' \'{print $10}\' | grep 9 | wc -l'
        cmd3 = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F' '\',\' \'{print $10}\' | grep 10 | wc -l'
        ret1 = commands.getstatusoutput(cmd1)
        ret2 = commands.getstatusoutput(cmd2)
        ret3 = commands.getstatusoutput(cmd3)
        return ret1[1],ret2[1],ret3[1] 

    def get_timeinterval_count(self):
        rets = []
        for hour in range(0,24):
            if hour < 10:
                hour = '0' + str(hour)
            else:
                hour = str(hour)
            cmd = 'cat ' + self.dict_set['VirusDir'] + '* | awk -F \',\' \'{print $8}\' | cut -c12-13 | grep ' + hour +    ' | wc -l' 
            ret = commands.getstatusoutput(cmd)
            rets.append(ret[1])
        return rets 

    def cmd_exec(self,cmd):
        ret_list = []
        if isinstance(cmd,list):
            for v in cmd:
                ret = commands.getstatusoutput(v)
                ret_list.append(ret[1])
            return ret_list 
        else:
            ret = commands.getstatusoutput(cmd)
            return ret[1]

    def w2f(self,content):
        path = self.dict_set['ResultFile'] + self.dict_set['DateStart'] + '_' + self.dict_set['DateEnd'][-2:] + '.csv'
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

    def get_virus_sm_src_c(self):
        cmd = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F \',\' \'{print $9}\' | sort | uniq | wc -l'
        return self.cmd_exec(cmd)

    def get_v_src_top6(self):
        cmd = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F \',\' \'{print $9}\' | cut -c1-4 | sort | uniq -c | sort -k1nr -k2 | head -6 | awk -F \' \' \'{print $2}\''
        return self.cmd_exec(cmd)

    def provin_take(self,state,bl,st,ed):
        if state == 'in':
            cmd = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | awk -F \' \' \'{if($2>=' + st + ' && $2<=' + ed + ')print $2}\' |wc -l'
        else:
            cmd = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | awk -F \' \' \'{if($2<' + st + ' || $2>' + ed + ')print $2}\' |wc -l'
        return cmd 

    def gd_provin_take(self,state,bl):
        if state == 'in':
            cmd = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | ' + 'awk -F \' \' \'{if($2==20 || ($2>=660&&$2<=668) || ($2>=750&&$2<=769))print $2}\'' + ' | wc -l'
        else:
            cmd = 'cat ' + self.dict_set['VirusDir'] + ' | awk -F \',\' \'{print $10\"hh\",$11}\' | grep ' + str(bl) +'hh | ' + 'awk -F \' \' \'{if($2!=20 && ($2<660||$2>668) && ($2<750||$2>769))print $2}\'' + ' | wc -l'
        return cmd 

    def get_provin_proportion(self):
        gd_state = self.dict_set['GdSet']
        if gd_state == 'ON':
            cmd_tele_in = self.gd_provin_take('in',2)
            cmd_tele_out = self.gd_provin_take('out',2)
            cmd_mobi_in = self.gd_provin_take('in',9,)
            cmd_mobi_out = self.gd_provin_take('out',9)
            cmd_uni_in = self.gd_provin_take('in',10)
            cmd_uni_out = self.gd_provin_take('out',10)
        else:
            st = self.dict_set['ProvinSt']
            ed = self.dict_set['ProvinEd']
            cmd_tele_in = self.provin_take('in',2,st,ed)
            cmd_tele_out = self.provin_take('out',2,st,ed)
            cmd_mobi_in = self.provin_take('in',9,st,ed)
            cmd_mobi_out = self.provin_take('out',9,st,ed)
            cmd_uni_in = self.provin_take('in',10,st,ed)
            cmd_uni_out = self.provin_take('out',10,st,ed)
        cmds =[cmd_tele_in,cmd_tele_out,cmd_mobi_in,cmd_mobi_out,cmd_uni_in,cmd_uni_out]
        return self.cmd_exec(cmds)

    def get_sm_alarm_tbname(self):
        st = self.dict_set['DateStart']
        tb_n = 'virus_sm_alarm_' + st[0:6]
        return tb_n

    def rm_blank_lines(self,path):
        cmd = 'sed -i \'/^$/d\' ' + path 
        self.cmd_exec(cmd)

    def bcp_load_apk_basic(self):
        db_version = self.dict_set['DatabaseVersion']
        if db_version == 'Oracle':
            cmd = 'bash shell/download_apk_basic_info.sh'
            self.cmd_exec(cmd)
        else:
            pw = self.dict_set['DatabasePWD']
            s_n = self.dict_set['DatabaseServer']
            db_n = self.dict_set['ApkBasicDbName']
            u_n = self.dict_set['DatabaseUser']
            tb_n = 'apk_basic_info'
            out_p = self.dict_set['RefDir'] + 'apk_basic_info.csv'
            cmd = 'bcp ' + db_n + '..' + tb_n + ' out ' + out_p + ' -U' + u_n + ' -P' + pw + ' -S' + s_n + ' -c -t\',\' -r\'\\n\''
            self.cmd_exec(cmd)
        self.rm_blank_lines(self.apk_basic_info_path)

    def bcp_load_sm_alarm(self):
        date = self.dict_set['DateStart'][0:6]
        db_version = self.dict_set['DatabaseVersion']
        if db_version == 'Oracle':
            cmd = 'bash shell/download_virus_sm_alarm.sh ' + date 
            self.cmd_exec(cmd)
        else:
            pw = self.dict_set['DatabasePWD']
            s_n = self.dict_set['DatabaseServer']
            db_n = self.dict_set['SmAlarmDbName']
            u_n = self.dict_set['DatabaseUser']
            tb_n = self.get_sm_alarm_tbname()
            out_p = self.dict_set['RefDir'] + tb_n + '.csv'
            cmd = 'bcp ' + db_n + '..' + tb_n + ' out ' + out_p + ' -U' + u_n + ' -P' + pw + ' -S' + s_n + ' -c -t\',\' -r\'\\n\''
            self.cmd_exec(cmd)
        self.rm_blank_lines(self.virus_alarm_path)

    def get_setting(self):
        dict_set = {}
        f = open('conf/setting.conf')
        for line in f:
            v = line.strip().split('=')
            if len(v) > 1:
                dict_set[v[0]] = v[1]
        f.close()
        return dict_set 

    def load_data(self):
        self.bcp_load_apk_basic()
        self.bcp_load_sm_alarm()
        self.get_url_details()
        self.get_virus_sm_detail()

    def overall_profile(self):
        #总体概括
        url_like_sm_c = self.get_count(self.dict_set['TarDir'] + '*')
        print 'url_like_sm_c=' + str(url_like_sm_c)
        virus_sm_c = self.get_count(self.dict_set['VirusDir'])
        print 'virus_sm_c=' + virus_sm_c
        virus_sm_reject_c = self.get_count(self.dict_set['VirusDir'] + ' | grep REJECT ')
        print 'virus_sm_reject_c=' + str(virus_sm_reject_c)
        out = '总体概括' + '\n'
        out += '带有网址或网址形态的短信总量,' + '病毒短信总量,' + '可拦截量' + '\n'
        out += str(url_like_sm_c) +',' +str(virus_sm_c) + ','+ str(virus_sm_reject_c) + '\n\n'
        self.w2f(out)

    def operator_distribution(self):
        #病毒短信各运营商分布
        telecom,mobile,unicom = self.get_phone_num_belong()
        print 'telecom=' + str(telecom)
        print 'mobile=' + str(mobile)
        print 'unicom=' + str(unicom)
        out = '病毒短信各运营商分布' + '\n'
        out += '电信' + ',' + '移动' + ',' + '联通' + '\n'
        out += str(telecom) + ',' + str(mobile) + ',' + str(unicom) + '\n\n'
        self.w2f(out)

    def timeinterval_send(self):
        #各时间段病毒短信发送量分布
        t_dev_list = self.get_timeinterval_count()        
        print 'timeinterval'
        print t_dev_list 
        out = '各时间段病毒短信发送量分布' + '\n'
        for i in range(0,24):
            out += str(i) + ','
        out += '\n'
        for v in t_dev_list:
            out += v + ','
        out += '\n\n'
        self.w2f(out)

    def src_sum(self):
        #病毒短信按主叫去重总数
        v_sms_src_c = self.get_virus_sm_src_c()
        print 'v_sms_src_c=' + str(v_sms_src_c) 
        out = '病毒短信按主叫去重总数' + '\n'
        out += str(v_sms_src_c) + '\n\n'
        self.w2f(out)

    def phonenum_top6(self):
        #病毒短信前6号段
        nub_list = self.get_v_src_top6()
        print 'nub_list'
        print nub_list 
        out = '病毒短信前6号段' + '\n'
        vs = nub_list.strip().split('\n')
        for v in vs:
            out += v + ','
        out += '\n\n'
        self.w2f(out)

    def provin_sent(self):
        #各运营商病毒短信省内外发送量占比
        provin_take_list = self.get_provin_proportion()
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
        self.w2f(out)

    def exec_shell_scrip(self,cmd):
        f = open('cmd.sh','w+')
        f.write(cmd)
        f.close()
        ret = self.cmd_exec('bash cmd.sh')
        self.cmd_exec('rm cmd.sh')
        return ret 

    def virus_type_sort(self):
        cmd = 'cat ' + self.dict_set['VirusDir'] + ' | grep -E \'视频|录相|录像|视屏\'' + ' | wc -l' 
        cmd2 = 'cat ' + self.dict_set['VirusDir'] + ' | grep -vE \'视频|录相|录像|视屏\'' +  ' | grep -E \'看|瞧|瞅\'' + ' | wc -l'
        cmd3 = 'cat ' + self.dict_set['VirusDir'] + ' | wc -l'
        video_type = int(self.exec_shell_scrip(cmd))
        photo_type = int(self.exec_shell_scrip(cmd2))
        all_type = int(self.exec_shell_scrip(cmd3))
        other_type = all_type - video_type - photo_type 
        v_t = float(1.0 * video_type/all_type)
        p_t = float(1.0 * photo_type/all_type)
        o_t = float(1.0 * other_type/all_type)
        out = '各类病毒短信占比情况' + '\n'
        out += '视频类,' + '相册类,' + '其它类,' + '\n' 
        out += str(video_type) + ',' + str(photo_type) + ',' + str(other_type) + '\n'
        out += str(v_t) + ',' + str(p_t) + ',' + str(o_t) + '\n\n'
        self.w2f(out)

    def virus_case_detail(self,tar,type):
        ip_dict = self.get_ip_map()
        cmd ='cat ' + self.dict_set['VirusDir'] + ' | ' + tar + ' | tail -1 | awk -F \',\' \'{print $4}\''
        url = self.cmd_exec(cmd)
        cmd ='cat ' + self.dict_set['VirusDir'] + ' | ' + tar + ' | tail -1 | awk -F \',\' \'{print $19}\''
        sms = self.cmd_exec(cmd) + url 
        sm_alarm_path = self.dict_set['RefDir'] + 'virus_sm_alarm_' + self.dict_set['DateStart'][0:6] + '.csv'
        cmd = 'cat ' + sm_alarm_path + ' | grep ' + url + ' | awk -F \',\' \'{print $12}\' | tail -1'
        ip = self.cmd_exec(cmd)
        if ip_dict.has_key(ip):
            ip_bl = ip_dict[ip]
        else:
            ip_bl = 'unknow'
        return [virus_type[type],url,sms,type_dict[type],ip,ip_bl]

    def case_show(self):
        v_cmd = 'grep -E \'视频|录相|录像|视屏\''
        v_type = self.virus_case_detail(v_cmd,2)
        p_cmd = 'grep -vE \'视频|录相|录像|视屏\'' +  ' | grep -E \'看|瞧|瞅\''
        p_type = self.virus_case_detail(p_cmd,1)
        o_cmd = 'grep -vE \'视频|录相|录像|视屏|看|瞧|瞅\''
        o_type = self.virus_case_detail(o_cmd,6)
        out = '病毒类型' + ',' + '病毒链接' + ',' + '病毒短信示例' + '恶意行为描述' + ',' + 'IP地址' + ',' + 'IP归属地' + '\n'
        self.w2f(out)
        self.w2f(v_type)
        self.w2f(p_type)
        self.w2f(o_type)

    def clear_pass(self):
        cmd = 'rm ' + self.dict_set['TarDir'] + '* ' + self.dict_set['RefDir'] + '* ' + self.dict_set['VirusDir'] 
        self.cmd_exec(cmd)

    def run(self):
        self.overall_profile()
        self.operator_distribution()
        self.timeinterval_send()
        self.src_sum()
        self.phonenum_top6()
        self.virus_type_sort()
        self.provin_sent()
        self.apk_belong()
        self.case_show()

obj = Statistics()
obj.clear_pass()
if sys.argv[1] == 'run':
    print 'begin to run.......'
    obj.load_data()
    obj.run()
else:
    print 'clear done!!!'
