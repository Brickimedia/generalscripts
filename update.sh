#!/bin/bash

echo "Updating Brickimedia 1.22"
echo "#############################"

skins=(Refreshed Custard DeepSea Quartz Lia)

for skin in ${skins[*]}
do
	echo "Updating "$skin
	cd /var/www/core/skins/$skin
	sudo git pull
done

echo "Updating extensions"
cd /var/www/core/extensions
sudo git pull
sudo git submodule init
sudo git submodule sync
sudo git submodule update

echo "Updating LocalSettings"
cd /var/www/core/
sudo git --git-dir=./LocalSettings.git pull origin master

echo "Updating splash"
cd /var/www/splash/
sudo git pull
