import pandas as pd
from zipfile import ZipFile
import tempfile
import shutil
import os
import filecmp

# https://www.palantir.com/docs/foundry/transforms-python/transforms-python-api-classes/#filesystem
# see here about random access file, which is what zip needs https://www.palantir.com/docs/foundry/transforms-python/unstructured-files/ 

def unnamed_2(site_569_omop_raw_zips):
    # site_569_omop_raw_zips is a TransformInput

    CHUNK_SIZE = 100 * 1024 * 1024
    zipfile_path = "cu-amc/incoming/CU-AMC_omop_20240103.zip"
    
    #zipfile_path = "cu-amc/incoming/CU-AMC_omop_20240122.zip"
    inputFS = site_569_omop_raw_zips.filesystem()
    zipfile_status = site_569_omop_raw_zips.filesystem().ls(glob=zipfile_path)
    # fetching the only file out of here.
    print(str(next(zipfile_status, "<no objects>")))
    # FileStatus(path='cu-amc/incoming/CU-AMC_omop_20240103.zip',
    #   size=201110311814,     modified=1705291231735)


    with tempfile.NamedTemporaryFile() as temp:
        # is it copied as a binary file? is it the same size?
        print(f"copying {zipfile_path} to {temp.name}")
        print(temp.name)
        print(os.stat(temp.name))
        # Copy contents of file from Foundry into temp file, ....needs to be able to seek()
        with inputFS.open(zipfile_path, 'rb') as newest:
            shutil.copyfileobj(newest, temp)
            temp.flush()
        temp_stat = os.stat(temp.name)
        print(f"TEMPFILE wrapper: {temp.name} {temp_stat}")
        # os.stat_result(st_mode=33152, st_ino=82465566, st_dev=1048808, st_nlink=1, 
        #.               st_uid=185, st_gid=0, 
        # st_size=201110311814, 
        #               st_atime=1706143388, st_mtime=1706145847, st_ctime=1706145847)
        # ===> the temp file is the same size as the original.
        # size, schmize.  Did the copy work right? diff would be nice. 
     #   print("FILECMP:", end = "")
     #   print(filecmp.cmp(temp.name, zipfile_path)) # this fails b/c temp path is relative?
     

        zipObj = ZipFile(temp.name)
        print("ZipFile object created")
        print("TESTZIP: ", end = "")
        try:
            print(zipObj.testzip())
        except Exception as x:
            print(f"testzip doesn't like the file: {x}")

        try:
            for zipinfo in zipObj.infolist():
                print(f"ZIPINFO: {zipinfo}")
        except Exception as x:
            print(f"couldn't create the infolist {x}")

        for filename in zipObj.namelist():
            file_length = 0
            try:
                input_file = zipObj.open(filename) # crashes here
                try:
                    data = input_file.read(CHUNK_SIZE)
                    file_length += len(data)
                    while data:
                        data = input_file.read(CHUNK_SIZE)
                        file_length += len(data)
                except Exception as y:
                    print(f"after open {filename} at {file_length} crashed with {y}")
            except Exception as x:
                print(f"file open {filename} crashed with {x}")
            print(f"  Final size for {filename}: {file_length}")

# successful log from 1/22 data:
#FileStatus(path='cu-amc/incoming/CU-AMC_omop_20240122.zip', size=187009280693, modified=1706088769772)
#copying cu-amc/incoming/CU-AMC_omop_20240122.zip to /tmp/tmpubdyf4_z
#/tmp/tmpubdyf4_z
#os.stat_result(st_mode=33152, st_ino=8530428, st_dev=1048703, st_nlink=1, st_uid=185, st_gid=0, st_size=0, st_atime=1706190097, st_mtime=1706190097, st_ctime=1706190097)
#TEMPFILE wrapper: /tmp/tmpubdyf4_z os.stat_result(st_mode=33152, st_ino=8530428, st_dev=1048703, st_nlink=1, st_uid=185, st_gid=0, st_size=187009280693, st_atime=1706190097, st_mtime=1706191969, st_ctime=1706191969)
#ZipFile object created
#TESTZIP: None
#ZIPINFO: <ZipInfo filename='DATAFILES/' external_attr=0x10>
#ZIPINFO: <ZipInfo filename='DATAFILES/CARE_SITE.csv' compress_type=deflate external_attr=0x20 file_size=202709 compress_size=27849>
#ZIPINFO: <ZipInfo filename='DATAFILES/CONDITION_ERA.csv' compress_type=deflate external_attr=0x20 file_size=5358956476 compress_size=1517010160>
#ZIPINFO: <ZipInfo filename='DATAFILES/CONDITION_OCCURRENCE.csv' compress_type=deflate external_attr=0x20 file_size=28124597275 compress_size=6674130282>
#ZIPINFO: <ZipInfo filename='DATAFILES/DEATH.csv' compress_type=deflate external_attr=0x20 file_size=3224886 compress_size=768362>
#ZIPINFO: <ZipInfo filename='DATAFILES/DEVICE_EXPOSURE.csv' compress_type=deflate external_attr=0x20 file_size=4693692028 compress_size=1197535671>
#ZIPINFO: <ZipInfo filename='DATAFILES/DRUG_ERA.csv' compress_type=deflate external_attr=0x20 file_size=6244954391 compress_size=1680665147>
#ZIPINFO: <ZipInfo filename='DATAFILES/DRUG_EXPOSURE.csv' compress_type=deflate external_attr=0x20 file_size=43586495326 compress_size=10113580543>
#ZIPINFO: <ZipInfo filename='DATAFILES/LOCATION.csv' compress_type=deflate external_attr=0x20 file_size=48638915 compress_size=5274883>
#ZIPINFO: <ZipInfo filename='DATAFILES/MEASUREMENT.csv' compress_type=deflate external_attr=0x20 file_size=189032409417 compress_size=50314611329>
#ZIPINFO: <ZipInfo filename='DATAFILES/NOTE.csv' compress_type=deflate external_attr=0x20 file_size=14658037017 compress_size=4128860747>
#ZIPINFO: <ZipInfo filename='DATAFILES/NOTE_NLP.csv' compress_type=deflate external_attr=0x20 file_size=483625322432 compress_size=86458366826>
#ZIPINFO: <ZipInfo filename='DATAFILES/OBSERVATION.csv' compress_type=deflate external_attr=0x20 file_size=77351939044 compress_size=18807904170>
#ZIPINFO: <ZipInfo filename='DATAFILES/OBSERVATION_PERIOD.csv' compress_type=deflate external_attr=0x20 file_size=106491524 compress_size=29646434>
#ZIPINFO: <ZipInfo filename='DATAFILES/PERSON.csv' compress_type=deflate external_attr=0x20 file_size=174685891 compress_size=29301480>
#ZIPINFO: <ZipInfo filename='DATAFILES/PROCEDURE_OCCURRENCE.csv' compress_type=deflate external_attr=0x20 file_size=6145692038 compress_size=1495074146>
#ZIPINFO: <ZipInfo filename='DATAFILES/PROVIDER.csv' compress_type=deflate external_attr=0x20 file_size=10457734 compress_size=1461576>
#ZIPINFO: <ZipInfo filename='DATAFILES/VISIT_DETAIL.csv' compress_type=deflate external_attr=0x20 file_size=4717451370 compress_size=959109140>
#ZIPINFO: <ZipInfo filename='DATAFILES/VISIT_OCCURRENCE.csv' compress_type=deflate external_attr=0x20 file_size=19164199036 compress_size=3595947365>
#ZIPINFO: <ZipInfo filename='DATA_COUNTS.csv' compress_type=deflate external_attr=0x20 file_size=474 compress_size=278>
#ZIPINFO: <ZipInfo filename='MANIFEST.csv' compress_type=deflate external_attr=0x20 file_size=467 compress_size=279>
#  Final size for DATAFILES/: 0
#  Final size for DATAFILES/CARE_SITE.csv: 202709
#  Final size for DATAFILES/CONDITION_ERA.csv: 5358956476
#  Final size for DATAFILES/CONDITION_OCCURRENCE.csv: 28124597275
#  Final size for DATAFILES/DEATH.csv: 3224886
#  Final size for DATAFILES/DEVICE_EXPOSURE.csv: 4693692028
#  Final size for DATAFILES/DRUG_ERA.csv: 6244954391
#  Final size for DATAFILES/DRUG_EXPOSURE.csv: 43586495326
#  Final size for DATAFILES/LOCATION.csv: 48638915
#  Final size for DATAFILES/MEASUREMENT.csv: 189032409417
#  Final size for DATAFILES/NOTE.csv: 14658037017
#  Final size for DATAFILES/NOTE_NLP.csv: 483625322432
#  Final size for DATAFILES/OBSERVATION.csv: 77351939044
#  Final size for DATAFILES/OBSERVATION_PERIOD.csv: 106491524
#  Final size for DATAFILES/PERSON.csv: 174685891
#  Final size for DATAFILES/PROCEDURE_OCCURRENCE.csv: 6145692038
#  Final size for DATAFILES/PROVIDER.csv: 10457734
#  Final size for DATAFILES/VISIT_DETAIL.csv: 4717451370
#  Final size for DATAFILES/VISIT_OCCURRENCE.csv: 19164199036
#  Final size for DATA_COUNTS.csv: 474
#  Final size for MANIFEST.csv: 467

# log from the Jan.02 file:
#FileStatus(path='cu-amc/incoming/CU-AMC_omop_20240103.zip', size=201110311814, modified=1705291231735)
#copying cu-amc/incoming/CU-AMC_omop_20240103.zip to /tmp/tmpuyd4kl7f
#/tmp/tmpuyd4kl7f
#os.stat_result(st_mode=33152, st_ino=66322436, st_dev=1048766, st_nlink=1, st_uid=185, st_gid=0, st_size=0, st_atime=1706207014, #st_mtime=1706207014, st_ctime=1706207014)
#TEMPFILE wrapper: /tmp/tmpuyd4kl7f os.stat_result(st_mode=33152, st_ino=66322436, st_dev=1048766, st_nlink=1, st_uid=185, #st_gid=0, st_size=201110311814, st_atime=1706207014, st_mtime=1706209026, st_ctime=1706209026)
#ZipFile object created
#TESTZIP: testzip doesn't like the file: [Errno 22] Invalid argument
#ZIPINFO: <ZipInfo filename='DATAFILES/' external_attr=0x10>
#ZIPINFO: <ZipInfo filename='DATAFILES/CARE_SITE.csv' compress_type=deflate external_attr=0x20 file_size=201898 compress_size=27742>
#ZIPINFO: <ZipInfo filename='DATAFILES/CONDITION_ERA.csv' compress_type=deflate external_attr=0x20 file_size=5263165924 compress_size=1489593488>
#ZIPINFO: <ZipInfo filename='DATAFILES/CONDITION_OCCURRENCE.csv' compress_type=deflate external_attr=0x20 file_size=27629289537 compress_size=6554484478>
#ZIPINFO: <ZipInfo filename='DATAFILES/DEATH.csv' compress_type=deflate external_attr=0x20 file_size=3130243 compress_size=745268>
#ZIPINFO: <ZipInfo filename='DATAFILES/DEVICE_EXPOSURE.csv' compress_type=deflate external_attr=0x20 file_size=4587088159 compress_size=1171042806>
#ZIPINFO: <ZipInfo filename='DATAFILES/DRUG_ERA.csv' compress_type=deflate external_attr=0x20 file_size=6131049699 compress_size=1648700465>
#ZIPINFO: <ZipInfo filename='DATAFILES/DRUG_EXPOSURE.csv' compress_type=deflate external_attr=0x20 file_size=42798065256 compress_size=9930384246>
#ZIPINFO: <ZipInfo filename='DATAFILES/LOCATION.csv' compress_type=deflate external_attr=0x20 file_size=48004121 compress_size=5205536>
#ZIPINFO: <ZipInfo filename='DATAFILES/MEASUREMENT.csv' compress_type=deflate external_attr=0x20 file_size=185741905579 compress_size=49465799137>
#ZIPINFO: <ZipInfo filename='DATAFILES/NOTE.csv' compress_type=deflate external_attr=0x20 file_size=18857441963 compress_size=5309598621>
#ZIPINFO: <ZipInfo filename='DATAFILES/NOTE_NLP.csv' compress_type=deflate external_attr=0x20 file_size=616372565372 compress_size=101213575530>
#ZIPINFO: <ZipInfo filename='DATAFILES/OBSERVATION.csv' compress_type=deflate external_attr=0x20 file_size=75986561595 compress_size=18476411187>
#ZIPINFO: <ZipInfo filename='DATAFILES/OBSERVATION_PERIOD.csv' compress_type=deflate external_attr=0x20 file_size=104665246 compress_size=29111699>
#ZIPINFO: <ZipInfo filename='DATAFILES/PERSON.csv' compress_type=deflate external_attr=0x20 file_size=172312542 compress_size=28908728>
#ZIPINFO: <ZipInfo filename='DATAFILES/PROCEDURE_OCCURRENCE.csv' compress_type=deflate external_attr=0x20 file_size=6034211492 compress_size=1468044537>
#ZIPINFO: <ZipInfo filename='DATAFILES/PROVIDER.csv' compress_type=deflate external_attr=0x20 file_size=10396659 compress_size=1453307>
#ZIPINFO: <ZipInfo filename='DATAFILES/VISIT_DETAIL.csv' compress_type=deflate external_attr=0x20 file_size=3509920788 compress_size=790925390>
#ZIPINFO: <ZipInfo filename='DATAFILES/VISIT_OCCURRENCE.csv' compress_type=deflate external_attr=0x20 file_size=18805415626 compress_size=3526426102>
#ZIPINFO: <ZipInfo filename='DATA_COUNTS.csv' compress_type=deflate external_attr=0x20 file_size=475 compress_size=278>
#ZIPINFO: <ZipInfo filename='MANIFEST.csv' compress_type=deflate external_attr=0x20 file_size=467 compress_size=283>
#file open DATAFILES/ crashed with [Errno 22] Invalid argument
#  Final size for DATAFILES/: 0
#file open DATAFILES/CARE_SITE.csv crashed with [Errno 22] Invalid argument
#  Final size for DATAFILES/CARE_SITE.csv: 0
#file open DATAFILES/CONDITION_ERA.csv crashed with [Errno 22] Invalid argument
#  Final size for DATAFILES/CONDITION_ERA.csv: 0
#file open DATAFILES/CONDITION_OCCURRENCE.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/CONDITION_OCCURRENCE.csv: 0
#file open DATAFILES/DEATH.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/DEATH.csv: 0
#file open DATAFILES/DEVICE_EXPOSURE.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/DEVICE_EXPOSURE.csv: 0
#file open DATAFILES/DRUG_ERA.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/DRUG_ERA.csv: 0
#file open DATAFILES/DRUG_EXPOSURE.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/DRUG_EXPOSURE.csv: 0
#file open DATAFILES/LOCATION.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/LOCATION.csv: 0
#file open DATAFILES/MEASUREMENT.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/MEASUREMENT.csv: 0
#file open DATAFILES/NOTE.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/NOTE.csv: 0
#file open DATAFILES/NOTE_NLP.csv crashed with Bad magic number for file header
#  Final size for DATAFILES/NOTE_NLP.csv: 0
#  Final size for DATAFILES/OBSERVATION.csv: 75986561595
#  Final size for DATAFILES/OBSERVATION_PERIOD.csv: 104665246
#  Final size for DATAFILES/PERSON.csv: 172312542
#  Final size for DATAFILES/PROCEDURE_OCCURRENCE.csv: 6034211492
#  Final size for DATAFILES/PROVIDER.csv: 10396659
#  Final size for DATAFILES/VISIT_DETAIL.csv: 3509920788
#  Final size for DATAFILES/VISIT_OCCURRENCE.csv: 18805415626
#  Final size for DATA_COUNTS.csv: 475
#  Final size for MANIFEST.csv: 467
  
