from zipfile import ZipFile

zipfile_name = "CU-AMC_omop_2040103.zip"

CHUNK_SIZE = 100 * 1024 * 1024
zipObj = ZipFile(zipfile_name)

for filename in zipObj.namelist():
    file_length = 0
    print(f"component file {filename} of zipfile {zipfile_name}")
    input_file = zipObj.open(filename) # crashes here
    data = input_file.read(CHUNK_SIZE)
    file_length += len(data)
    while data:
        data = input_file.read(CHUNK_SIZE)
        file_length += len(data)
    printf(f"  Final size for {filename}: {file_length}")

