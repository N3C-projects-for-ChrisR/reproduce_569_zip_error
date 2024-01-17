
# Reproducing the zip error in Site 569

## Running the Code
All scripts require 7zip. Available at  https://www.7-zip.org/download.html
- make_zip_file.sh explores 7zip flags  
- make_zip_2.sh creates files of different sizes to create different errors involving running out of disk space.
  - It requires a small filesystem, here /Volumes/tiny, so you can run out of space.
  - The script takes arguments for different failing scenarios A, B, and C, as well as one that runs cleanly X.
- make_zip_3.sh is like make_zip_2.sh but uses unzip_n3c_2.py
- I've been doing this on macos Sonoma 14.2.1

<blockquote>
<pre>
bash> make_zip_2.sh A
</pre>
</blockquote>


## python scripts
- unzip.py is the original from the enclave
- unzip_n3c.py is a simplified version that uses python to pull out the files individually. It does not use the python utilities to do the file copies.
- unzip_n3c_2.py is more complicated, but doesn't use the small file system, and as of now, fails to reproduce anything  interesting.

## Stack Dump
Traceback (most recent call last):
<blockquote>
<pre>
  File "/app/work-dir/_environment_/lib/python3.8/site-packages/transforms/build.py", line 378, in run
    self._transform.compute(ctx=transform_context, **parameters)
  File "/app/work-dir/__environment_/lib/python3.8/site-packages/transforms/api/transform.py", line 301, in compute
    self(**kwargs)
  File "/app/work-dir/__environment_/lib/python3.8/site-packages/transforms/api/transform.py", line 216, in __call_
    return self.compute_func(*args, **kwargs)
  File "/app/work-dir/__environment_/lib/python3.8/site-packages/myproject/datasets/step00_unzip/unzip.py", line 12, in unzip
    unzipLatest(zip_file, regex, unzipped)
  File "/app/work-dir/_environment_/lib/python3.8/site-packages/source_cdm_utils/unzip.py", line 22, in unzipLatest
    unzip(foundryZip, foundryOutput, newest_file)
  File "/app/work-dir/_environment_/lib/python3.8/site-packages/source_cdm_utils/unzip.py", line 40, in unzip
    input_file = zipObj.open(filename)
  File "/app/work-dir/_environment_/lib/python3.8/zipfile.py", line 1530, in open
    fheader = zef_file.read(sizeFileHeader)
  File "/app/work-dir/_environment_/lib/python3.8/zipfile.py", line 763, in read
    self._file.seek(self._pos)
OSError: [Errno 22] Invalid argument
</pre>
</blockquote>

## CPython source is here;
git@github.com:python/cpython.git
Lib/zipfile.py

### line 763, the failing one, is      "self._file.seek(self._pos)"
The _pos comes from the header length, calculated from the struct module: 
<blockquote>
<pre>
  stringEndArchive = b"PK\005\006"
  structEndArchive = b"<4s4H2LH"
  sizeEndCentDir = struct.calcsize(structEndArchive)
</pre>
</blockquote>
The structEndArchive string can be decoded with instructions here under "Format Strings". https://docs.python.org/3/library/struct.html
It workds out to 30 bytes which agrees with the filename of the first included file starting at byte 31. The 'a' menioned in  make_zip_file.sh.
I went down this path because I saw a different header.


