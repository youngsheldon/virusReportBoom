#!/bin/bash
sqlplus -s smmcadmin/AdminDB^12@SMMC <<EOF
set colsep ,  
set feedback off  
set heading off  
set trimout on
set linesize 2048
set newp none 
spool data_sort/ref_data/apk_basic_info.csv 
select code||','||name||','||MD5||','||SHA1||','||SHA256||','||SHA512||','||first_found||','||last_update||','||short_url||','||long_url||','||content||','||risk||','||category||','||cost||','||low_config||','||better_config||','||init_ip||','||init_ip_attribution||','||target_ip||','||target_ip_attribution||','||apk_file_size||','||apk_source_num  from apk_basic_info;
spool off
EOF