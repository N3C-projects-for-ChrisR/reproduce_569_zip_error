#!/usr/bin/env bash
#set -euo pipefail

# make_zip_2.sh
#   Trying to reproduce the failure of unzipping the zip file Site 569 is sending in.
#    They use 7zip, as used here to create the file kahn.zip.  Simply unzipping files
#    created this way with the Python code in the enclave works.
#
#    Speculation here is that it involves limited file space.
#    This script shows the error messages in these scenarios.
#    - X: plenty space to run through zip creation, copy and extraction
#    - A: not enough space to create the zip file
#    - B: not enough space to copy the zip file
#    - C: not enough space to unzip the file
#    The differen scenarios are created in a filesystem with just 1GB of space 
#    by creating file 'c' in different sizes.
#
# Some setup is required. The errors created here depend on having a 
# directory in a file system with space limited to 1gb, specified in DATA_HOME.
#
# RESULTS: I have not been able to re-produce the error seen in the enclave.
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
ls -lht $DATA_HOME

echo "copy (bash)"
cp kahn.zip kahn2.zip
sleep $SLEEP_DURATION 

#$PROJECT_HOME/7zz x kahn2.zip
##unzip kahn2.zip
echo "extract (python)"
$PROJECT_HOME/unzip_n3c.py $DATA_HOME/kahn2.zip
