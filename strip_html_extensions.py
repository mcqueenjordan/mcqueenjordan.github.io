import os
from glob import glob

for f in glob('./_site/*.html'):
    os.rename(f, f.replace('.html', ''))
