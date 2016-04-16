mysqldump -u root njtransit > $(( NJTRANSIT_COUNTER )).sql;
(( NJTRANSIT_COUNTER++ ));
echo $(( NJTRANSIT_COUNTER ));
mysql -u root njtransit < ../sql/reset.sql;