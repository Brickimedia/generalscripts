#!/bin/bash

echo "Updating Brickimedia 1.20"
echo "#############################"

locations=("/var/www" "/media/MediaWikiChat" "/media/NewTalkGlobal" "/media/SocialProfile" "/var/www/wiki/skins/Refreshed" "/media/Custard" "/var/www/wiki/skins/Quartz" "/var/www/wiki/skins/DeepSea" "/media/GlobalContribs" "/var/www/wiki/extensions/NumberOfComments" )

for path in ${locations[*]}
do
  file=`echo $path | rev | cut -d/ -f1 | rev`
  echo "Running update for "$file"..."
  cd $path
  git pull
done

echo "Complete!"

#1.22 updates
echo
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
git submodule update

echo "Updating LocalSettings"
cd /var/www/core/
git --git-dir=./LocalSettings.git pull origin master