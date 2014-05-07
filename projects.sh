#!/bin/bash

#runs the given script on all wikis in our farm

WIKIS=(meta dev en customs stories ideas admin data nl answers books)

for wiki in $WIKIS
do
echo "performing on " $wiki
`WIKI=$wiki $1`
done
