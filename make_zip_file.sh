#!/usr/bin/env bash
set -euo pipefail

rm -rf junk
rm -f od_outputs
dd if=/dev/zero of=a bs=10m count=1
dd if=/dev/zero of=b bs=10m count=1
dd if=/dev/urandom of=c bs=10m count=1


zip basic.zip a b c

# These three are the same
#./7zz a kahn.zip -tzip -mx=3 -mm=Deflate -mnt=4  a b c
./7zz a kahn.zip -tzip -mx=3 -mm=Deflate  a b c
./7zz a seven.zip a b c
./7zz a seven_8.zip -tzip -mx=3 -mm=8  a b c # Deflate

# These are different
./7zz a seven_0.zip -tzip -mx=3 -mm=0  a b c # store (no compression)
# eight is above
./7zz a seven_9.zip -tzip -mx=3 -mm=9  a b c # Deflate64 
./7zz a seven_12.zip -tzip -mx=3 -mm=12  a b c # bzip2
./7zz a seven_14.zip -tzip -mx=3 -mm=14  a b c # LZMA

# Same
diff seven.zip seven_8.zip

mkdir junk
cd junk

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
set +euo
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

echo "kahn.zip"
od -c kahn.zip | head -3

echo "basic.zip"
od -c basic.zip | head -3
