create table virus_report_summarize
(
    id               int,
    date_time        date,
    url_like_count   int,
    virus_sum_count  int,
    reject_sum_count int,
    tele_in_count    int,
    tele_out_count   int,
    mobile_in_count  int,
    mobile_out_count int,
    union_in_count   int,
    union_out_count  int,
    src_uniq_count   int,
    video_type_count int,
    album_type_count int,
    other_type_count int,
    constraint v_r_s_pk primary key(id) 
);

create sequence v_r_s_tb_seq minvalue 1 maxvalue 99999999
increment by 1
start with 1;   
create or replace trigger v_r_s_tb_tri
before insert on virus_report_summarize     
for each row                      
begin                                
select v_r_s_tb_seq.nextval into :new.id from dual; 
end;

create table virus_period_send
(
    id               int,
    date_time        date,
    t0_c             int,
    t1_c             int,
    t2_c             int,
    t3_c             int,
    t4_c             int,
    t5_c             int,
    t6_c             int,
    t7_c             int,
    t8_c             int,
    t9_c             int,
    t10_c            int,
    t11_c            int,
    t12_c            int,
    t13_c            int,
    t14_c            int,
    t15_c            int,
    t16_c            int,
    t17_c            int,
    t18_c            int,
    t19_c            int,
    t20_c            int,
    t21_c            int,
    t22_c            int,
    t23_c            int,
    constraint v_p_s_pk primary key(id)
);

create sequence v_p_s_tb_seq minvalue 1 maxvalue 99999999
increment by 1
start with 1;   
create or replace trigger v_p_s_tb_tri
before insert on virus_period_send     
for each row                      
begin                                
select v_p_s_tb_seq.nextval into :new.id from dual; 
end;

create table src_segment_top6
(
    id               int,
    date_time        date,
    seg0             varchar(4),
    seg1             varchar(4),
    seg2             varchar(4),
    seg3             varchar(4),
    seg4             varchar(4),
    seg5             varchar(4),
    constraint s_s_t_pk primary key(id)
);

create sequence s_s_t_tb_seq minvalue 1 maxvalue 99999999
increment by 1
start with 1;   
create or replace trigger s_s_t_tb_tri
before insert on src_segment_top6     
for each row                      
begin                                
select s_s_t_tb_seq.nextval into :new.id from dual; 
end;

create table virus_type_example 
(
    id               int,
    date_time        date,
    type             int,
    url              varchar(256),
    sm_text          varchar(580),
    ip               varchar(16),
    ip_attribution   varchar(80),
    constraint v_t_e_pk primary key(id)
);

create sequence v_t_e_tb_seq minvalue 1 maxvalue 99999999
increment by 1
start with 1;   
create or replace trigger v_t_e_tb_tri
before insert on virus_type_example     
for each row                      
begin                                
select v_t_e_tb_seq.nextval into :new.id from dual; 
end;

create table url_ip_relate
(
    id               int,
    date_time        date,
    url              varchar(256),
    send_count       int,
    ip               varchar(16),
    ip_attribution   varchar(80),
    constraint u_i_r_pk primary key(id)
);

create sequence u_i_r_tb_seq minvalue 1 maxvalue 99999999
increment by 1
start with 1;   
create or replace trigger u_i_r_tb_tri
before insert on url_ip_relate     
for each row                      
begin                                
select u_i_r_tb_seq.nextval into :new.id from dual; 
end;

create table victim_distribution
(
       id int not null,
       url varchar(512),
       city varchar(60),
       constraint v_d_pk primary key(id) 
);
create sequence v_d_tb_seq minvalue 1 maxvalue 99999999
increment by 1
start with 1;   
create or replace trigger v_d_tb_tri
before insert on victim_distribution     
for each row                      
begin                                
select v_d_tb_seq.nextval into :new.id from dual; 
end;

CREATE OR REPLACE PROCEDURE sp_vir_victim_distribution
(
  url_t  in varchar,  --病毒URL
  city_t       in varchar --城市区号
) is
col smallint;
begin
  select count(*) into col from victim_distribution where url = url_t and city = city_t;
  if col = 0 then 
    insert into victim_distribution (url,city)values (url_t,city_t);
  end if;
end;

create table virus_source_rec 
(
   id                   varchar(25)                    not null,
   urlGrade             int,
   urlCode              varchar(8),
   url                  varchar(128),
   nti_code             varchar(24),
   msgid                varchar(10),
   smcid                int,
   recv_time            date,
   src                  varchar(21),
   src_type             int,
   src_locate           int,
   dst                  varchar(21),
   dst_type             int,
   dst_locate           int,
   state                varchar(7),
   alarm_type           int,
   alarm_resp           varchar(20),
   hash                 varchar(32),
   nosymbol             varchar(140),
   content              varchar(580)
);

CREATE OR REPLACE PROCEDURE sp_vir_source_rec
(
   id_t          in   varchar,
   urlGrade_t    in   int,
   urlCode_t     in   varchar,
   url_t         in   varchar,
   nti_code_t    in   varchar,
   msgid_t       in   varchar,
   smcid_t       in   int,
   recv_time_t   in   date,
   src_t         in   varchar,
   src_type_t    in   int,
   src_locate_t  in   int,
   dst_t         in   varchar,
   dst_type_t    in   int,
   dst_locate_t  in   int,
   state_t       in   varchar,
   alarm_type_t  in   int,
   alarm_resp_t  in   varchar,
   hash_t        in   varchar,
   nosymbol_t    in   varchar,
   content_t     in   varchar
) is
col smallint;
flag smallint;
begin
   select count(*) into col from virus_source_rec where url = url_t;
   if col = 0 then 
      insert into virus_source_rec values (id_t,urlGrade_t,urlCode_t,url_t,nti_code_t,msgid_t,smcid_t,recv_time_t,src_t,src_type_t,src_locate_t,dst_t,dst_type_t,dst_locate_t,state_t,alarm_type_t,alarm_resp_t,hash_t,nosymbol_t,content_t);
   elsif col > 0 then 
      select count(*) into flag from virus_source_rec where url = url_t and to_date(recv_time_t,'YYYY-MM-DD HH24:MI:SS') < recv_time;
      if flag > 0 then 
         delete from virus_source_rec where url = url_t;
         insert into virus_source_rec values (id_t,urlGrade_t,urlCode_t,url_t,nti_code_t,msgid_t,smcid_t,recv_time_t,src_t,src_type_t,src_locate_t,dst_t,dst_type_t,dst_locate_t,state_t,alarm_type_t,alarm_resp_t,hash_t,nosymbol_t,content_t);
      end if;
   end if;
end;