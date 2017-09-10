#!/bin/zsh

source .env

echo "Building jekyll _site/ contents..."
jekyll build &&

python3 script/deploy_website.py

