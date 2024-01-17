#!/usr/bin/env bash
#set -euo pipefail

# make_zip_3.sh
# see make_zip_2.sh, this changes the copy and unzip steps at the end.
# FAILS to attempt to reproduce properly because this new code uses the /tmp
# filesystem that is much larger than /Volumes/tiny, so the scenarios don't work.
#
# Chris Roeder, Jan. 2024

if [[ "$1" == "X" || "$1" == "A" || "$1" == "B" || "$1" == "C" ]] ; then
    SCENARIO=$1
else
    SCENARIO='A'
    echo "usage: make_zip_2.sh <scenario>"
    echo "  Where scenario is one of A, B, C, or X "
fi
echo "scenario: $SCENARIO"
    
SLEEP_DURATION=5
PROJECT_HOME=/Users/roederc/work/git_n3c/569_zip/
DATA_HOME=/Volumes/tiny

cd $DATA_HOME

# cleanup
rm -rf junk
rm -rf $DATA_HOME/*.zip a b c

# create fake data
dd if=/dev/zero of=a bs=10m count=1 > /dev/null 2> /dev/null
dd if=/dev/zero of=b bs=10m count=2 > /dev/null 2> /dev/null

if [[ "$SCENARIO" == 'X' ]]; then
    # X: leave space
    dd if=/dev/urandom of=c bs=10m count=10 > /dev/null 2> /dev/null  # copy doesn't complete. Without set -e, we continue to the unzip
    # [[no error]]
fi

if [[ "$SCENARIO" == 'A' ]]; then
    # A: too little space to create first zip
    dd if=/dev/urandom of=c bs=10m count=57 > /dev/null 2> /dev/null # fails when creating first zip
    # errno=28 : No space left on device
    # cp: kahn.zip: No such file or directory
    #FileNotFoundError: [Errno 2] No such file or directory: '/Volumes/tiny/kahn2.zip'
fi

if [[ "$SCENARIO" == 'B' ]]; then
    # B: too little space to copy the zip file
    dd if=/dev/urandom of=c bs=10m count=37 > /dev/null 2> /dev/null # fails when creating/writing second zip
    #: kahn2.zip: fcopyfile failed: No space left on device
    #zipfile.BadZipFile: File is not a zip file

fi

if [[ "$SCENARIO" == 'C' ]]; then
    # C: not enough to unzip
    dd if=/dev/urandom of=c bs=10m count=32 > /dev/null 2> /dev/null # copy doesn't complete. Without set -e, we continue to the unzip
    ls -lht  $DATA_HOME
    echo "rm"
    # OSError: [Errno 28] No space left on device
fi

echo "zip"
${PROJECT_HOME}/7zz a kahn.zip -tzip -mx=3 -mm=Deflate  a b c > /dev/null
if [[ "$SCENARIO" == 'C' ]]; then
    rm a b c
fi
sleep $SLEEP_DURATION 
echo $DATA_HOME
ls -lht $DATA_HOME


## This version copies and unzips in python instead of copying in bash then calling pyton to unzip
$PROJECT_HOME/unzip_n3c_2.py $DATA_HOME/kahn.zip




