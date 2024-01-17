#!/usr/bin/env python3

'''

The get_newest_payload() and extract_filenames() functions are not great and should be re-written someday.
- tschwab

'''
import sys
import os
from zipfile import ZipFile

# Read and write 100 MB chunks
CHUNK_SIZE = 100 * 1024 * 1024


def unzip(filename):
    # Create a temp file to pass to zip library, because it needs to be able to .seek()
        zipObj = ZipFile(filename)
        for filename in zipObj.namelist():
            with open(filename, 'wb') as out:
                input_file = zipObj.open(filename)
                data = input_file.read(CHUNK_SIZE)
                while data:
                    out.write(data)
                    data = input_file.read(CHUNK_SIZE)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        unzip(sys.argv[1])
    else:
        print("usage: unzip_n3c <filename>") 


