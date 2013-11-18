#!/bin/bash

echo "Brickimedia automatic updater"
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
