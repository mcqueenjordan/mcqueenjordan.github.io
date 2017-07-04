import os
import boto3
import datetime
from glob import glob

PDX = 'us-west-2'
s3 = boto3.client('s3', region_name = PDX)
cloudfront = boto3.client('cloudfront')

WEBSITE_BUCKET_NAME = os.environ['WEBSITE_BUCKET_NAME']
CLOUDFRONT_DISTRIBUTION_ID = os.environ['CLOUDFRONT_DISTRIBUTION_ID']

GENERATED_SITE_DIR = '_site'
THOUGHT_DIR = '{}/thought'.format(GENERATED_SITE_DIR)
HTML = '.html'
FILES_TO_KEEP_HTML_EXTENSIONS = {
        '_site/googleadb73ac2a3c3efa7.html'
        }

CONTENT_TYPE_MAPPING = {
        'css': 'text/css',
        'txt': 'text/plain'
        }

def main() -> None:
    print("Re-organizing /thought/ structure...")
    reorganize_thought_file_structure()

    print("Stipping all .html extensions (except blacklisted files).")
    strip_extensions_recursively(GENERATED_SITE_DIR, HTML)

    print("Uploading all files to S3...")
    upload_website_to_s3(GENERATED_SITE_DIR, WEBSITE_BUCKET_NAME)

    print("Invalidating all CloudFront caches. (TODO: only invalidate changes.)")
    invalidate_caches()


def reorganize_thought_file_structure() -> None:
    pattern = '{}/**/*.html'.format(THOUGHT_DIR)
    for f in glob(pattern, recursive = True):
        thought_name = f.split('/')[-2]
        new_name = '{}/{}.html'.format(THOUGHT_DIR, thought_name)
        os.rename(f, new_name)
        os.rmdir(new_name[:-5])


def strip_extensions_recursively(root: str, extension: str) -> None:
    pattern = '{}/**/*{}'.format(root, extension)
    for f in glob(pattern, recursive = True):
        if f not in FILES_TO_KEEP_HTML_EXTENSIONS:
            os.rename(f, f.replace(extension, ''))


def upload_website_to_s3(directory: str, s3_bucket_name: str) -> None:
    pattern = '{}/**/*'.format(directory)
    for filename in glob(pattern, recursive = True):
        if os.path.isdir(filename): continue

        s3_object_key = '/'.join(filename.split('/')[1:])
        content_type = decide_content_type(filename)

        with open(filename, 'rb') as f:
                s3.put_object(
                        Body = f,
                        Bucket = s3_bucket_name,
                        ContentType = content_type,
                        Key = s3_object_key
                        )

        print('Uploaded: {} to {}/{}'.format(filename, s3_bucket_name, s3_object_key))


def decide_content_type(filename: str) -> str:
    extension = filename.split('.')[-1]
    return CONTENT_TYPE_MAPPING.get(extension, 'text/html')


def invalidate_caches() -> None:
    cloudfront.create_invalidation(
            DistributionId = CLOUDFRONT_DISTRIBUTION_ID,
            InvalidationBatch = {
                'Paths': {
                    'Items': ['/*'],
                    'Quantity': 1
                    },
                'CallerReference': str(datetime.datetime.now())
                }
            )

if __name__ == '__main__':
    main()

