#!/usr/bin/env python3

# https://stackoverflow.com/questions/65016185/python-f-seek-caused-oserror-errno-22-if-manually-edit-the-text-file-but-no-er

import os
import sys
scenario='B'
FILENAME="junk_file"

if (len(sys.argv) > 1):
    scenario=sys.argv[1]
else:
    print("usage why_22_from_seek.py <scenario>")
    exit()


os.system(f"dd if=/dev/zero of={FILENAME} bs=10m count=1 > /dev/null 2> /dev/null")

if scenario == 'A':
    with open(FILENAME, "rb") as f:
        f.seek(-2)
        print(f.readline())

if scenario == 'B':
    os.system(f"truncate -s 30 {FILENAME}")
    os.system(f"wc -c {FILENAME}")
    with open(FILENAME, "rb") as f:
        f.seek(29)
        print(f.readline())

if scenario == 'C':
    os.system(f"truncate -s 30 {FILENAME}")
    os.system(f"wc -c {FILENAME}")
    with open(FILENAME, "rb") as f:
        f.seek(31)
        print(f.readline())

if scenario == 'D':
    os.system(f"truncate -s 30 {FILENAME}")
    os.system(f"wc -c {FILENAME}")
    with open(FILENAME, "rb") as f:
        f.seek(0)
        print(f.readline())

if scenario == 'E':
    os.system(f"truncate -s 30 {FILENAME}")
    os.system(f"wc -c {FILENAME}")
    with open(FILENAME, "rb") as f:
        f.seek(-1)
        print(f.readline())



