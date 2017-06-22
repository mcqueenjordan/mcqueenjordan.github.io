source .env

echo "Building jekyll _site/ contents..."
jekyll build &&

# I don't like .html endings in URLs. Remove them.
python3.6 strip_html_extensions.py &&

echo "Pushing to S3..."
# Because we removed the extensions, we push the content-type text/html.
aws s3 sync ./_site $WEBSITE_BUCKET_NAME --content-type "text/html"
