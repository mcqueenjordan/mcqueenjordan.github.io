source .env

echo "Building jekyll _site/ contents"
jekyll build &&

echo "Pushing to S3"
aws s3 sync ./_site $WEBSITE_BUCKET_NAME
