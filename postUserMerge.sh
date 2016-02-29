#!/bin/sh

# change directory to MW maintenance
cd /var/www/core/maintenance

# inputs
read -p "Username/IP to transfer from: " fromuser
read -p "Username/IP to transfer to: " touser

# all wikis
WIKIS=(meta dev en fanatics stories ideas admin data answers books minifigures)

# execute
for wiki in $WIKIS
do
  echo "Reassigning edits from" $fromuser "to" $touser "on" $wiki
  WIKI=$wiki php reassignEdits.php $fromuser $touser
done
