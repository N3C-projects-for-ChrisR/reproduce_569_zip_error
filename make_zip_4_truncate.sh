#!/usr/bin/env bash
#set -euo pipefail

# make_zip_4.sh
# Use another tool to truncate the zip file instead of having happen by accident of the file system size.#
# no copying eihhter. Just one scenario.
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
truncate -s -29 kahn.zip # not a zip file # 29 bytes shorter
#truncate -s 29 kahn.zip # not a zip file # exactly 29 bytes long
#runcate -s 30 kahn.zip # not a zip file
#truncate -s 31 kahn.zip # not a zip file
#truncate -s 32 kahn.zip # not a zip file
ls -lt a  b c kahn.zip
$PROJECT_HOME/unzip_n3c.py kahn.zip
