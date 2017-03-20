#!/bin/bash
sqlplus -s smmcadmin/AdminDB^12@SMMC <<EOF
set colsep ,  
set feedback off  
set heading off  
set trimout on
set linesize 2048
set newp none 
spool data_sort/ref_data/virus_sm_alarm_$1.csv
select code||','||recv_time||','||sm_text||','||nnos_hash||','||sm_count||','||src_addr_count||','||dst_addr_count||','||url||','||Surl||','||Eurl||','||Sip||','||target_ip||','||file_md5||','||authority||','||probability||','||alarm_time||','||alarm_grade||','||alarm_code||','||virus_flag from virus_sm_alarm_$1;
spool off
EOF