#!/bin/bash
sqlplus -s smmcadmin/AdminDB^12@SMMC <<EOF
# set trimspool on 
# set linesize 1024
# set pagesize 2000 
# set heading off 
# set term off 
set newp none
set colsep ,
set echo off
set feedback off
set heading off
set pagesize 0
set termout off
set trimout on
set trimspool on
set linesize 1024
spool data_sort/ref_data/apk_basic_info.csv 
select code||','||name||','||MD5||','||SHA1||','||SHA256||','||SHA512||','||first_found||','||last_update||','||short_url||','||long_url||','||content||','||risk||','||category||','||cost||','||low_config||','||better_config||','||init_ip||','||init_ip_attribution||','||target_ip||','||target_ip_attribution||','||apk_file_size||','||apk_source_num  from apk_basic_info;
spool off
EOF