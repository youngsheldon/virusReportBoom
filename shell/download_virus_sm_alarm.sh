#!/bin/bash
sqlplus -s smmcadmin/AdminDB^12@SMMC <<EOF
set trimspool on 
set linesize 1024
set pagesize 2000 
set heading off 
set term off 
spool data_sort/ref_data/virus_sm_alarm_$1.csv
select code||','||recv_time||','||sm_text||','||nnos_hash||','||src_addr_count||','||dst_addr_count||','||url||','||Surl||','||Eurl||','||Sip||','||target_ip||','||file_md5||','||probability||','||alarm_time||','||alarm_grade||','||alarm_code||','||virus_flag from virus_sm_alarm_$1;
spool off
EOF