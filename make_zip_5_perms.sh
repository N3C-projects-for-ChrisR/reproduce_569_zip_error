#!/usr/bin/env bash
#set -euo pipefail

# make_zip_5.sh
# Maybe I'm fixated on file-size and it's permissions. Google "OSEerror invalid argument 22"
# Maybe, it gives what you'd expect: PermissionError: [Errno 13] Permission denied: 'kahn.zip'
# 
# Chris Roeder, Jan. 2024

PROJECT_HOME=/Users/roederc/work/git_n3c/569_zip/


# cleanup
rm -rf kahn.zip a b c

# create fake data
dd if=/dev/zero of=a bs=10m count=1 > /dev/null 2> /dev/null
dd if=/dev/zero of=b bs=10m count=2 > /dev/null 2> /dev/null
dd if=/dev/urandom of=c bs=10m count=10 > /dev/null 2> /dev/null  # copy doesn't complete. Without set -e, we continue to the unzip

${PROJECT_HOME}/7zz a kahn.zip -tzip -mx=3 -mm=Deflate  a b c > /dev/null
ls -lt kahn.zip
echo ""
chmod 000 kahn.zip
ls -lt a  b c kahn.zip
$PROJECT_HOME/unzip_n3c.py kahn.zip
