#!/bin/bash

now=$(date +"%A")
rm -rf /var/www/wiki/backups/$now
mkdir -p /var/www/wiki/backups/$now

#Source file for database passwords
source /media/backups/pass.sh

databases=(shared meta en customs stories cuusoo admin dev globalblocking)

echo "backing up dbs"

for db in ${databases[*]}
do
	echo "backing up " $db
	mysqldump -h localhost --user=$dbuser --password=$dbpass $db | gzip > /media/backups/$now/$db.sql.gz --force

done
