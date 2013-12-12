#!/bin/bash

echo "Updating Brickimedia 1.22"
echo "#############################"

skins=(Refreshed Custard DeepSea Quartz Lia)

for skin in ${skins[*]}
do
	echo "Updating "$skin
	cd /var/www/core/skins/$skin
	git pull
done

echo "Updating extensions"
cd /var/www/core/extensions
git pull
git submodule init
git submodule sync
git submodule update

echo "Updating LocalSettings"
cd /var/www/core/
git --git-dir=./LocalSettings.git pull origin master