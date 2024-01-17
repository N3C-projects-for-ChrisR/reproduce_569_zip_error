#!/usr/bin/env python3

'''
Similar to unzip_n3c.py, this unzips the way it's done in the enclave. 
This is closer because it includes a temp file copy of the zip file.
'''
import sys
import os
from zipfile import ZipFile
import tempfile
import shutil

# Read and write 100 MB chunks
#CHUNK_SIZE = 100 * 1024 * 1024
# Read and write 1 MB chunks
CHUNK_SIZE = 1024 * 1024


def unzip(filename):
    with tempfile.NamedTemporaryFile() as temp:
        with open(filename, 'rb') as newest:
            shutil.copyfileobj(newest, temp)
            temp.flush()

        zipObj = ZipFile(temp.name)
        for included_filename in zipObj.namelist():
            with open(included_filename, 'wb') as out:
                input_file = zipObj.open(included_filename)
                data = input_file.read(CHUNK_SIZE)
                while data:
                    out.write(data)
                    data = input_file.read(CHUNK_SIZE)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        unzip(sys.argv[1])
    else:
        print("usage: unzip_n3c <filename>") 




