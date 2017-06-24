import os
import boto3
from glob import glob

PDX = 'us-west-2'
s3 = boto3.client('s3', region_name = PDX)
WEBSITE_BUCKET_NAME = os.environ['WEBSITE_BUCKET_NAME']
GENERATED_SITE_DIR = '_site'
THOUGHT_DIR = '{}/thought'
HTML = '.html'

def main() -> None:
    reorganize_thought_file_structure()
    strip_extensions_recursively(GENERATED_SITE_DIR, HTML)
    upload_website_to_s3(GENERATED_SITE_DIR, WEBSITE_BUCKET_NAME)

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
        os.rename(f, f.replace(extension, ''))

def upload_website_to_s3(directory: str, s3_bucket_name: str) -> None:
    pattern = '{}/**/*'.format(directory)
    for filename in glob(pattern, recursive = True):
        if os.path.isdir(filename): continue

        if filename.endswith('.css'):
            content_type = 'text/css'
        else:
            content_type = 'text/html'

        s3_object_key = '/'.join(filename.split('/')[1:])

        with open(filename, 'rb') as f:
                s3.put_object(
                        Body = f,
                        Bucket = s3_bucket_name,
                        ContentType = content_type,
                        Key = s3_object_key
                        )

        print('Uploaded: {} to {}/{}'.format(filename, s3_bucket_name, s3_object_key))

if __name__ == '__main__':
    main()
