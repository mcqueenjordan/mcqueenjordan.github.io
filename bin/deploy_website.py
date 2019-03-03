import os
import boto3
import datetime
import sys
import hashlib
import htmlmin
from collections import Counter
from typing import List
from glob import glob
import concurrent.futures

PDX = 'us-west-2'
s3 = boto3.client('s3', region_name = PDX)
cloudfront = boto3.client('cloudfront')

WEBSITE_BUCKET_NAME = os.environ['WEBSITE_BUCKET_NAME']
CLOUDFRONT_DISTRIBUTION_ID = os.environ['CLOUDFRONT_DISTRIBUTION_ID']

S3_ETAG_HASHING_BLOCK_SIZE = 10240
MAX_UPLOAD_THREADS = 32
GENERATED_SITE_DIR = '_site'
THOUGHT_DIR = '{}/thought'.format(GENERATED_SITE_DIR)
THING_DIR = '{}/thing'.format(GENERATED_SITE_DIR)
IGNORED_DIRS = {'bin'}
FILES_TO_KEEP_HTML_EXTENSIONS = {
        '_site/googlec2238860c55ca6af.html'
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
    print("Re-organizing file structures...")
    reorganize_file_structures([THOUGHT_DIR, THING_DIR])

    print("Cleaning all file extensions (except blacklisted files) to look pretty in URIs.")
    html_files = prettify_filenames_recursively(GENERATED_SITE_DIR, '.html')

    print("Minifying HTML files...")
    minify_html_files(html_files)

    print("Uploading changed files to S3...")
    new_s3_keys = upload_website_to_s3(GENERATED_SITE_DIR, WEBSITE_BUCKET_NAME)

    print("Invalidating all CloudFront caches. (TODO: only invalidate {}.)".format(new_s3_keys))
    invalidate_caches()

def reorganize_file_structures(dir_roots) -> None:
    for dir_root in dir_roots:
        pattern = '{}/**/*.html'.format(dir_root)
        for f in glob(pattern, recursive = True):
            name = f.split('/')[-2]
            new_name = '{}/{}.html'.format(dir_root, name)
            os.rename(f, new_name)
            os.rmdir(new_name[:-5])

def prettify_filenames_recursively(root: str, extension: str) -> None:
    html_files = strip_extensions_recursively(root, '.html')
    lower_case_of_extensions('{}/photos/'.format(root), '.JPG')
    return html_files

def strip_extensions_recursively(root: str, extension: str) -> None:
    affected_files = []
    pattern = '{}/**/*{}'.format(root, extension)
    for f in glob(pattern, recursive = True):
        # TODO(jqq): conceptually, this check belongs outside this function
        if f not in FILES_TO_KEEP_HTML_EXTENSIONS:
            new_name = f.replace(extension, '')
            os.rename(f, new_name)
            affected_files.append(new_name)
    return affected_files

def lower_case_of_extensions(root: str, extension: str) -> None:
    pattern = '{}/**/*{}'.format(root, extension)
    for f in glob(pattern, recursive = True):
        os.rename(f, f.replace(extension, extension.lower()))

def minify_html_files(html_files):
    for html_file in html_files:
        with open(html_file, 'r') as f:
            minified = htmlmin.minify(f.read(), remove_comments = True,
                                      reduce_boolean_attributes = True,
                                      remove_empty_space = True)
        with open(html_file, 'w') as f:
            f.write(minified)

def upload_file(filename: str, s3_bucket_name: str) -> None:
    if not is_file_changed(filename, s3_bucket_name):
        return None

    content_type = decide_content_type(filename)

    with open(filename, 'rb') as f:
            s3.put_object(
                    Body = f,
                    Bucket = s3_bucket_name,
                    ContentType = content_type,
                    ContentDisposition = 'inline',
                    Key = get_s3_key_from_filename(filename)
                    )
    return get_s3_key_from_filename(filename)

def get_s3_key_from_filename(filename: str) -> str:
    return '/'.join(filename.split('/')[1:])

def is_file_changed(filename: str, s3_bucket_name: str) -> bool:
    '''
    Compares local and remote hashes, returning True if equal, False otherwise.
    '''
    local_hash = calculate_local_etag(filename)
    try:
        metadata = s3.head_object(Bucket = s3_bucket_name, Key = get_s3_key_from_filename(filename))
        remote_hash = metadata['ResponseMetadata']['HTTPHeaders']['etag'].strip("'\"")
    except Exception as e:
        # There are lots of potential failure modes here, but we'll just assume
        # return True is an OK implementation for now. Can tune if necessary.
        print(e)
        return True

    return remote_hash != local_hash

def upload_website_to_s3(directory: str, s3_bucket_name: str) -> None:
    pattern = '{}/**/*'.format(directory)
    filenames = get_uploadable_files(glob(pattern, recursive = True))

    with concurrent.futures.ThreadPoolExecutor(max_workers = MAX_UPLOAD_THREADS) as executor:
        results = []
        futures = [
            executor.submit(upload_file, f, s3_bucket_name) for f in filenames]

        for future in concurrent.futures.as_completed(futures, timeout = 512):
            if future.result() is not None:
                results.append(future.result())

        print("Uploaded {} files: {}".format(len(results), results))
        return results

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

def calculate_local_etag(path):
    '''
    This is a proxy of S3s implementation to calculate the etag for
    single-part objects.

    Note that multi-part uploaded objects will hash differently than this
    function on S3s service, so we cannot rely on hash comparisons if the
    S3 object was multi-part uploaded.
    '''
    with open(path, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(S3_ETAG_HASHING_BLOCK_SIZE)
            if len(data) == 0:
                break
            m.update(data)
        return m.hexdigest()

if __name__ == '__main__':
    main()

