# Previous Python code was not from Michael Kahn.
# This code is from Michael Kahn
# It successfully extracts all files from an actual N3C zip file created by 7Zip
# Including a 480GB NOTE_NLP CSV file

# This code extracts a ZIP file using the ZipFile.extractall() method

import zipfile
import os

#zip_file_path = 'test.zip'
zip_file_path = 'CU-AMC_omop_20240103.zip'
extracted_directory = 'extracted_files'

# Create the extraction directory if it doesn't exist.
if not os.path.exists(extracted_directory):
    os.makedirs(extracted_directory)

# Open the ZIP file for reading.
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Extract all the files in the ZIP file to the specified directory.
    zip_ref.extractall(extracted_directory)
print(f'All files from {zip_file_path} have been extracted to {extracted_directory}.')
