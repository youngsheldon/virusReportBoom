#!/bin/bash
sqlplus -s smmcadmin/AdminDB^12@SMMC <<EOF
@$1;
EOF
