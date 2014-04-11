#!/bin/bash

now=$(date +"%A")
rm -rf /media/backups/$now
mkdir -p /media/backups/$now

#Source file for database passwords
source /media/backups/pass.sh

databases=(shared meta en customs stories cuusoo admin dev globalblocking data)

echo "backing up dbs"

/home/nxt/.dropbox-dist/dropboxd & #start dropbox incase it has been stopped

for db in ${databases[*]}
do
        echo "backing up " $db
        mysqldump -h localhost --user=$dbuser --password=$dbpass $db | gzip > /media/backups/$now/$db.sql.gz --force
        cp -f /media/backups/$now/$db.sql.gz /home/nxt/Dropbox/backups/$db.sql.gz
done
