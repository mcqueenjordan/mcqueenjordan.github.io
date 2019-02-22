import os
import boto3
import datetime
from typing import List
from glob import glob
import concurrent.futures

PDX = 'us-west-2'
s3 = boto3.client('s3', region_name = PDX)
cloudfront = boto3.client('cloudfront')

WEBSITE_BUCKET_NAME = os.environ['WEBSITE_BUCKET_NAME']
CLOUDFRONT_DISTRIBUTION_ID = os.environ['CLOUDFRONT_DISTRIBUTION_ID']

GENERATED_SITE_DIR = '_site'
THOUGHT_DIR = '{}/thought'.format(GENERATED_SITE_DIR)
IGNORED_DIRS = {'bin'}
FILES_TO_KEEP_HTML_EXTENSIONS = {
        '_site/googleadb73ac2a3c3efa7.html'
        }
CONTENT_TYPE_MAPPING = {
        'css': 'text/css',
        'txt': 'text/plain',
        'JPG': 'image/jpeg',
        'jpg': 'image/jpeg',
        'ico': 'image/x-icon',
        'pdf': 'application/pdf',
        'svg': 'image/svg+xml'
        }


def main() -> None:
    print("Re-organizing /thought/ structure...")
    reorganize_thought_file_structure()

    print("Cleaning all file extensions (except blacklisted files) to look pretty in URIs.")
    prettify_filenames_recursively(GENERATED_SITE_DIR, '.html')

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


def prettify_filenames_recursively(root: str, extension: str) -> None:
    strip_extensions_recursively(root, '.html')
    lower_case_of_extensions('{}/photos/'.format(root), '.JPG')


def strip_extensions_recursively(root: str, extension: str) -> None:
    pattern = '{}/**/*{}'.format(root, extension)
    for f in glob(pattern, recursive = True):
        if f not in FILES_TO_KEEP_HTML_EXTENSIONS:
            os.rename(f, f.replace(extension, ''))

def lower_case_of_extensions(root: str, extension: str) -> None:
    pattern = '{}/**/*{}'.format(root, extension)
    for f in glob(pattern, recursive = True):
        os.rename(f, f.replace(extension, extension.lower()))

def upload_file(filename: str, s3_bucket_name: str) -> None:
    s3_object_key = '/'.join(filename.split('/')[1:])
    content_type = decide_content_type(filename)

    with open(filename, 'rb') as f:
            s3.put_object(
                    Body = f,
                    Bucket = s3_bucket_name,
                    ContentType = content_type,
                    ContentDisposition = 'inline',
                    Key = s3_object_key
                    )
    print('Uploaded: {} to {}/{}'.format(filename, s3_bucket_name, s3_object_key))

def upload_website_to_s3(directory: str, s3_bucket_name: str) -> None:
    pattern = '{}/**/*'.format(directory)
    filenames = get_uploadable_files(glob(pattern, recursive = True))

    with concurrent.futures.ThreadPoolExecutor(max_workers = 32) as executor:
        futures = [
            executor.submit(upload_file, f, s3_bucket_name) for f in filenames]

        for future in concurrent.futures.as_completed(futures, timeout = 512):
            # We could print more here, but no need. Just a simple way to
            # BLOCK until all future tasks complete.
            pass


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

def get_uploadable_files(filenames: List[str]) -> List[str]:
    allowed_files = []
    for filename in filenames:
        try:
            dirname = filename.split('/')[1]
        except:
            pass
        if dirname not in IGNORED_DIRS and not os.path.isdir(filename):
            allowed_files.append(filename)
    return allowed_files

if __name__ == '__main__':
    main()

