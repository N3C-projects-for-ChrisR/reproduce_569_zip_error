
# Reproducing the zip error in Site 569

## 7zip available here: https://www.7-zip.org/download.html\

## python scripts
- unzip.py is the original from the enclave
- unzip_n3c.py is a simplified version that uses python to pull out the files individually. It does not use the python utilities to do the file copies.
- TODO use a more complex python script that uses python to copy files

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


## Scripts
- make_zip_2.sh
- make_zip_file.sh
