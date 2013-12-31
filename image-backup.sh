#!/bin/sh

cd /var/www
 
#backup destination
dest="/media/backup/bm-images"

day=$(date +%S)
archive_file="bm-images-$day.tgz"

echo "Backing up images to $dest/$archive_file"

tar czf $dest/$archive_file "/var/www/images"

echo "Backup finished"
