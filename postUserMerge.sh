#!/bin/sh

# change directory to MW maintenance
cd /var/www/core/maintenance

# inputs
read -p "Wiki to operate on: " usewiki
read -p "Username/IP to transfer from: " fromuser
read -p "Username/IP to transfer to: " touser

# execute
WIKI=$usewiki php reassignEdits.php $fromuser $touser
