import os
from glob import glob

def main() -> None:
    reorganize_nested_thoughts()
    strip_extensions_recursively('_site', '.html')

def reorganize_nested_thoughts() -> None:
    for f in glob('./_site/thought/**/*.html', recursive = True):
        thought_name = f.split('/')[-2]
        new_name = './_site/thought/{}.html'.format(thought_name)
        os.rename(f, new_name)
        os.rmdir(new_name[:-5])

def strip_extensions_recursively(root: str, extension: str) -> None:
    for f in glob('./{}/**/*{}'.format(root, extension), recursive = True):
        os.rename(f, f.replace(extension, ''))

if __name__ == '__main__':
    main()
