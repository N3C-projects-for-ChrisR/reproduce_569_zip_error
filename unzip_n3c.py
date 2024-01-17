#!/usr/bin/env python3

'''
  This is the way the n3c enclave unzips a file, component by component, chunk by chunk.
'''
import sys
import os
from zipfile import ZipFile

# Read and write 100 MB chunks
#CHUNK_SIZE = 100 * 1024 * 1024
# Read and write 1 MB chunks
CHUNK_SIZE =  1024 * 1024


def unzip(filename):
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


