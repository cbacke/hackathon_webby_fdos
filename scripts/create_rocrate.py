#!/usr/bin/env python3

import glob
from pathlib import Path

from rocrate.rocrate import ROCrate

PROJECT_ROOT = Path(__file__).parent.parent
ROCRATE_EXPORT_ROOT = PROJECT_ROOT / 'rocrate_export'
RAW_FILESIZES_PATH = PROJECT_ROOT / 'input/file_sizes.txt'

FILETREE_ROOT = PROJECT_ROOT / 'filetree'
DATA_ROOT = FILETREE_ROOT  / 'data'

FILESIZES = {}
with open(RAW_FILESIZES_PATH) as f:
    for line in f:
        size_bytes_raw, _, relpath_raw = line.strip().partition(' ')
        size_bytes = int(size_bytes_raw)
        relpath = tuple(relpath_raw[2:].split('/'))
        FILESIZES[relpath] = size_bytes

def get_encoding_format(filename):
    # TODO: Add proper format names. See:
    # https://www.researchobject.org/ro-crate/specification/1.1/data-entities.html
    # https://schema.org/encodingFormat
    # https://www.iana.org/assignments/media-types/media-types.xhtml
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/MIME_types

    formats = {
        'csv': 'text/csv',
        'jpg': 'image/jpeg',
        'json': 'application/json',
        'md': 'text/markdown',
        'png': 'image/png',
        'sh': '...',            # TODO
        'sqlite': '...',        # TODO
        'txt': 'text/plain',
        'asc': 'text',          # TODO
    }
    try:
        encoding_format = formats[filename.suffix.lstrip('.')]
    except KeyError:
#        print(f'No encoding format for this file: {filename}')
        encoding_format = ''
    return encoding_format

def main():
    crate = ROCrate()
    crate.datePublished = 'foo'
    # crate.add()   # zip archives have PIDs and public URLs
    data_filepaths = [
        Path(p).relative_to(FILETREE_ROOT)
        for p in glob.glob(str(DATA_ROOT / '*/*/*/*'))]
    print(len(data_filepaths))
    for data_filepath in data_filepaths:
        filesize = FILESIZES[data_filepath.parts]
        crate.add_file(
            FILETREE_ROOT / data_filepath,
            dest_path=data_filepath,
            properties={
                'name': str(data_filepath),
                'contentSize': filesize,
                'encodingFormat': get_encoding_format(data_filepath),
            })

    crate.write(ROCRATE_EXPORT_ROOT)

if __name__ == '__main__':
    main()
