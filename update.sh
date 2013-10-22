#!/bin/bash

echo "Brickimedia automatic updater"
echo "#############################"

locations=("/var/www" "/media/MediaWikiChat" "/media/NewTalkGlobal" "/media/NewTalkGlobal" "/media/SocialProfile" "/media/Refreshed" "/media/Custard")

for path in ${locations[*]}
do
  file=`echo $path | rev | cut -d/ -f1 | rev`
  echo "Running update for "$file"..."
  cd $path
  git pull
done

echo "Complete!"
