select name, id from "group" where name in (
    'south-african-environmental-observation-network',
    'saeon-observations-database');
                      name                       |                  id                  
-------------------------------------------------+--------------------------------------
 south-african-environmental-observation-network | 5f385b66-4ef1-4312-9435-7923eecbc6a8
 saeon-observations-database                     | d8012844-3c27-472a-a205-19adefb1666a
(2 rows)
delete from member_revision where group_id not in ('5f385b66-4ef1-4312-9435-7923eecbc6a8', 'd8012844-3c27-472a-a205-19adefb1666a');
delete from member where group_id not in ('5f385b66-4ef1-4312-9435-7923eecbc6a8', 'd8012844-3c27-472a-a205-19adefb1666a');
delete from group_extra_revision where group_id not in ('5f385b66-4ef1-4312-9435-7923eecbc6a8', 'd8012844-3c27-472a-a205-19adefb1666a');
delete from group_extra where group_id not in ('5f385b66-4ef1-4312-9435-7923eecbc6a8', 'd8012844-3c27-472a-a205-19adefb1666a');
delete from group_revision where id not in ('5f385b66-4ef1-4312-9435-7923eecbc6a8', 'd8012844-3c27-472a-a205-19adefb1666a');
delete from "group" where id not in ('5f385b66-4ef1-4312-9435-7923eecbc6a8', 'd8012844-3c27-472a-a205-19adefb1666a');
delete from package_extra_revision where package_id not in (
    select p.id from package p join package_extra e on p.id = e.package_id and e.key = 'metadata_collection_id'
    where p.owner_org = '5f385b66-4ef1-4312-9435-7923eecbc6a8'
    and e.value = 'd8012844-3c27-472a-a205-19adefb1666a');
delete from package_extra where package_id not in (
    select p.id from package p join package_extra e on p.id = e.package_id and e.key = 'metadata_collection_id'
    where p.owner_org = '5f385b66-4ef1-4312-9435-7923eecbc6a8'
    and e.value = 'd8012844-3c27-472a-a205-19adefb1666a');
delete from package_revision where id not in (
    select p.id from package p join package_extra e on p.id = e.package_id and e.key = 'metadata_collection_id'
    where p.owner_org = '5f385b66-4ef1-4312-9435-7923eecbc6a8'
    and e.value = 'd8012844-3c27-472a-a205-19adefb1666a');
delete from package where id not in (
    select p.id from package p join package_extra e on p.id = e.package_id and e.key = 'metadata_collection_id'
    where p.owner_org = '5f385b66-4ef1-4312-9435-7923eecbc6a8'
    and e.value = 'd8012844-3c27-472a-a205-19adefb1666a');