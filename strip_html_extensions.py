import os
from glob import glob

for f in glob('./_site/**/*.html', recursive = True):
    os.rename(f, f.replace('.html', ''))
