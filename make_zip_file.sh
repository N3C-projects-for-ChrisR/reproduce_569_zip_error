#!/usr/bin/env bash
set -euo pipefail

# make_zip_file.sh
#
# The basic goal here is to get the flags to 7zz right and see
# how what it creates is compatible with zip.
# The error we're trying to reproduce from the enclave invovles calling a seek()
# to the end of the zip file header, making the headers suspect. As written,
# this script creates files with headers of the same length that agree with
# the calculation.....
#
# The script:
# - Creates zip files using different tools and flags. 
# - Tests unziping them using "unzip", showing failures with incompatible zip types.

# - Shows headers of files. 
#   - Note the first four bytes, the magic number: "P K 003 004"
#   - Note the filename of the first file in the archive  in the second to last position 
#     of the second row 'a'. The header is 30 bytes.
#  0000000    P   K 003 004 024  \0  \0  \0  \b  \0 345   P   1   X 314   *
#  0000020    ʞ  ** 316   '  \0  \0  \0  \0 240  \0 001  \0 034  \0   a   U
#  0000040    T  \t  \0 003   >  \t 250   e   >  \t 250   e   u   x  \v  \0
#
#

PROJECT_HOME=/Users/roederc/work/git_n3c/569_zip
DATA_HOME=/Volumes/tiny

cd $DATA_HOME
rm -rf junk
rm -rf $DATA_HOME/*.zip
dd if=/dev/zero of=a bs=10m count=1 > /dev/null 2> /dev/null
dd if=/dev/zero of=b bs=10m count=1 > /dev/null 2> /dev/null
dd if=/dev/urandom of=c bs=10m count=1 > /dev/null 2> /dev/null


zip basic.zip a b c

# These three are the same
$PROJECT_HOME/7zz a kahn.zip -tzip -mx=3 -mm=Deflate  a b c > /dev/null 2> /dev/null
$PROJECT_HOME/7zz a seven.zip a b c > /dev/null 2> /dev/null
$PROJECT_HOME/7zz a seven_8.zip -tzip -mx=3 -mm=8  a b c # Deflate > /dev/null 2> /dev/null
# The -mnt flag fails. I assume is irrelevant because it specifies the number of threads to use.
#$PROJECT_HOME/7zz a kahn.zip -tzip -mx=3 -mm=Deflate -mnt=4  a b c

# These are different
$PROJECT_HOME/7zz a seven_0.zip -tzip -mx=3 -mm=0  a b c > /dev/null 2> /dev/null # store (no compression)
# eight is above
$PROJECT_HOME/7zz a seven_9.zip -tzip -mx=3 -mm=9  a b c > /dev/null 2> /dev/null # Deflate64 
$PROJECT_HOME/7zz a seven_12.zip -tzip -mx=3 -mm=12  a b c > /dev/null 2> /dev/null # bzip2
$PROJECT_HOME/7zz a seven_14.zip -tzip -mx=3 -mm=14  a b c > /dev/null 2> /dev/null # LZMA

# Same
diff seven.zip seven_8.zip
echo "diff seven.zip seven_8.zip  $?"
diff seven.zip kahn.zip
echo "diff seven.zip kahn.zip  $?"

mkdir junk
cd junk
########> /dev/null 2> /dev/null

# Fails 
#unzip ../seven.7zip # fails, not a zip file

# works
unzip ../seven.zip
ls
rm -f *

# works
unzip ../seven_0.zip
ls
rm -f *

# Fails, not compat
#unzip ../seven_12.zip

# Fails, not compat
# unzip ../seven_14.zip

# work
unzip ../seven_8.zip
ls
rm -f *
unzip ../seven_9.zip
ls
rm -f *


cd ..
set +euo 2> /dev/null > /dev/null
#od -c seven.7zip | head -3

echo "seven.zip"
od -c seven.zip | head -3

echo "seven_0.zip"
od -c seven_0.zip | head -3

#od -c seven_12.zip | head -3
#od -c seven_14.zip | head -3

echo "seven_8.zip"
od -c seven_8.zip | head -3

echo "seven_9.zip"
od -c seven_9.zip | head -3

echo "basic.zip"
od -c basic.zip | head -3

echo "seven_12.zip"
od -c seven_12.zip | head -3

echo "seven_14.zip"
od -c seven_14.zip | head -3


