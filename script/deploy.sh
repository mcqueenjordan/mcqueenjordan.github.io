#!/bin/zsh

source .env

echo "Building jekyll _site/ contents..."
jekyll build &&

python3.6 script/deploy_website.py

