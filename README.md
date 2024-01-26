
# Reproducing the zip error in Site 569

Many scripts require 7zip. Available at  https://www.7-zip.org/download.html

## files and experiments
- make_zip_file.sh explores different commands and flags for creating zip files.
- unzip.py is a copy of the enclave code. It depends on the Palantir environment.
- abbreviated_n3c_unzip.py This is a basic Python script to use the zipfile package to open, list and read component files from a zip file. It doesn't write them because the errors we've seen happen before that. Python script, not a zip program because we're duplicating, at least in part, what is done in the enclave.
- unzip_n3c_2.py This is a simplification of unzip.py that can run outside of Foundry or Spark to exercise just ZipFile.
- why_22_from_seek.py This script calls open(), a function used by ZipFile that appears in the error from it, to find what can reproduce that specific erorr: OSError: [Errno 22] Invalid argument
- This is a series of attempts to mangle the zip file and reproduce the error message indirectly through ZipFile.
  - make_zip_2.sh, make_zip_3.sh
    - Both requires a small filesystem, here /Volumes/tiny, so you can run out of space.  
  - make_zip_4_truncate.sh
  - make_zip_5_perms.sh
- final_enclave.py Is the final code run on the enclave. It has log output from both a failing and a successful run.

## tweak_zip.c experiment
This code reads in a zipfile created from file_d, file_e, and file_f to change some of the offsets to negative values in hopes of re-creating the error "Invalid argument" message. The first attempt got me:     raise BadZipFile("Truncated file header")
- create the zip file: zip good.zip file_d file_e file_f
- create a character dump of it: od -c good.zip
- create an octal dump of shorts of it: od -x good.zip
- compare that output to what is in good.txt
- compile and run tweak_zip: gcc tweak.zip; ./a.out
    - it will read good.zip and write gooder.zip
- create the dumps and compare to the previous ones. 
- test the new file with zip: unzip gooder.zip
- test the new file with the python snippet: abbreviated_n3c_unzip.py gooder.zip


## Stack Dump
This is the stack dump from the enclave failure. This is what I want to reproduce.
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

 line 763, the failing one, is      "self._file.seek(self._pos)"
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

See also https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html



