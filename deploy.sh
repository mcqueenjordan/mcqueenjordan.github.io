source .env

echo "Building jekyll _site/ contents..."
jekyll build &&

python3.6 deploy_website.py

