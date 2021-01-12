#!/usr/bin/env bash

GIT_USER='penteor'
GIT_BRANCH='main'

echo '[*] Saving VIRTUALENV libraries in requirements.txt file'
pip freeze --local > requirements.txt

echo '[*] Select Branch: ' $GIT_BRANCH ' for user:' $GIT_USER
git checkout $GIT_BRANCH

echo '[*] Push code to Branch:' $GIT_BRANCH
unixtime=$(date +%s)
git add --all
git commit -m $unixtime
git push -f origin $GIT_BRANCH
git tag $unixtime
git push --tags