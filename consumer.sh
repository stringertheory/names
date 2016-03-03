#!/bin/bash
wget --output-file=wget.log --input-file=Dropbox/poems-urls.txt --no-clobber --wait=0.5 --random-wait --directory-prefix=Dropbox/html
