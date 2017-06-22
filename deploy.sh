source .env

echo "Building jekyll _site/ contents..."
jekyll build &&

python3.6 strip_html_extensions.py &&

echo "Pushing to S3..."
aws s3 sync ./_site $WEBSITE_BUCKET_NAME --content-type "text/html"
