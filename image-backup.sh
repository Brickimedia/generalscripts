#!/bin/sh

cd /var/www
 
#backup destination
dest="/media/backup/bm-images"

day=$(date +%A)
archive_file="bm-images-$day.tgz"

echo "Backing up images to $dest/$archive_file"

tar czf $dest/$archive_file "./wiki/images"

echo "Backup finished"
