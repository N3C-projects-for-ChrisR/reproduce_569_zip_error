#!/usr/bin/env python3

# This is a snippet I sent to michael to see if Python could read his zip file.
# It exercises the failing open() call, but does not actually extract the files, saving diskspace.

from zipfile import ZipFile
import sys

#zipfile_name="CU-AMC_omop_20240103.zip"
if (len(sys.argv) > 1):
    zipfile_name=sys.argv[1]
else:
    print("usage: abbreviated_n3c_unzip.py <filename>")
CHUNK_SIZE = 100 * 1024 * 1024

zipObj = ZipFile(zipfile_name)
for filename in zipObj.namelist():
        file_length=0
        input_file = zipObj.open(filename) ### crashes here
        data = input_file.read(CHUNK_SIZE)
        file_length += len(data)
        while data:
            data = input_file.read(CHUNK_SIZE)
            file_length += len(data)
        print(f"component file {filename} of zipfile {zipfile_name} length {file_length} chunk size: {CHUNK_SIZE} ")
