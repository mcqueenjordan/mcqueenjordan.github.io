#!/bin/zsh

source .env

echo "Building jekyll _site/ contents..."
bundle exec jekyll build &&

python3 bin/deploy_website.py

