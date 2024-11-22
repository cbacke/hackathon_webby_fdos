#!/usr/bin/env python3

import glob
from pathlib import Path

from rocrate.rocrate import ROCrate

PROJECT_ROOT = Path(__file__).parent.parent

ROCRATE_EXPORT_ROOT = PROJECT_ROOT / 'rocrate_export'
RAW_FILESIZES_PATH = PROJECT_ROOT / 'input/file_sizes.txt'
FILETREE_ROOT = PROJECT_ROOT / 'filetree'
DATA_ROOT = FILETREE_ROOT  / 'data'
SPEC_ROOT = FILETREE_ROOT  / 'specification'
LGBK_ROOT = FILETREE_ROOT  / 'logbook'

FILESIZES = {}
with open(RAW_FILESIZES_PATH) as f:
    for line in f:
        size_bytes_raw, _, relpath_raw = line.strip().partition(' ')
        size_bytes = int(size_bytes_raw)
        relpath = tuple(relpath_raw[2:].split('/'))
        FILESIZES[relpath] = size_bytes

def get_filesize(data_filepath, is_dummy=True):
    if is_dummy:
        return FILESIZES[data_filepath.parts]
    return data_filepath.stat().st_size

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
#        'sh': '...',            # TODO
#        'sqlite': '...',        # TODO
        'txt': 'text/plain',
#        'asc': 'text',          # TODO
    }
    try:
        encoding_format = formats[filename.suffix.lstrip('.')]
    except KeyError:
        encoding_format = ''
        print(f'No encoding format for this file: {filename}')
#        raise
    return encoding_format

def main():
    crate = ROCrate()
    crate.datePublished = '2024-06-26'

    crate.root_dataset['identifier'] = 'https://doi.org/10.5281/zenodo.12547116'

    # TODO: zip archives have PIDs and public URLs
    crate.add_file(
        FILETREE_ROOT / 'data.zip',
        fetch_remote=False,
        properties={
            'contentUrl': 'https://zenodo.org/records/12547116/files/data.zip',
            'contentSize': 4579311616,
            'encodingFormat': 'application/zip'
        }
    )
#    crate.add_file(
#        FILETREE_ROOT / 'specification.zip',
#        dest_path='specification.zip',
#        properties={
#            'url': 'https://doi.org/10.5281/zenodo.12547116',
#            'contentSize': 4579311616,
#            'encodingFormat': 'application/zip'
#        }
#    )
#
    # Data filepaths
    data_filepaths = [
        Path(p).relative_to(FILETREE_ROOT)
        for p in glob.glob(str(DATA_ROOT / '*/*/*/*'))]
#    print(len(data_filepaths))
    for data_filepath in data_filepaths:
        crate.add_file(
            FILETREE_ROOT / data_filepath,
            dest_path=data_filepath,
            properties={
                'name': str(data_filepath),
                'contentSize': get_filesize(data_filepath),
                'encodingFormat': get_encoding_format(data_filepath),
            })

    # Experiment specification filepaths
    exp_spec_filepaths = [
        exp_spec_filepath
        for bundle in [[
            (SPEC_ROOT / 'experiment/experiment.md').relative_to(FILETREE_ROOT)], [
            (SPEC_ROOT / 'parameter/parameter.json').relative_to(FILETREE_ROOT)], [
            Path(p).relative_to(FILETREE_ROOT)
                for p in glob.glob(str(
                    SPEC_ROOT / 'experiment/*/*-description.md'))], [
            Path(p).relative_to(FILETREE_ROOT)
                for p in glob.glob(str(
                    SPEC_ROOT / 'experiment/*/*.json'))], [
            Path(p).relative_to(FILETREE_ROOT)
                for p in glob.glob(str(
                    SPEC_ROOT / 'experiment/*/img/*.png'))
            ]]
        for exp_spec_filepath in bundle
    ]

#    ).extend([
#        SPEC_ROOT / 'experiment/experiment.md']).extend([
#        SPEC_ROOT / 'parameter/parameter.json']).extend([
#        Path(p).relative_to(FILETREE_ROOT)
#            for p in glob.glob(str(
#                SPEC_ROOT / 'experiment/*/*-description.md'))]).extend([
#        Path(p).relative_to(FILETREE_ROOT)
#            for p in glob.glob(str(
#                SPEC_ROOT / 'experiment/*/*.json'))]).extend([
#        Path(p).relative_to(FILETREE_ROOT)
#            for p in glob.glob(str(
#                SPEC_ROOT / 'experiment/*/img/*.png'))])
    for exp_spec_filepath in exp_spec_filepaths:
        crate.add_file(
            FILETREE_ROOT / exp_spec_filepath,
            dest_path=exp_spec_filepath,
            properties={
                'name': str(exp_spec_filepath),
                'contentSize': get_filesize(exp_spec_filepath),
                'encodingFormat': get_encoding_format(exp_spec_filepath),
            })

    # Export the complete rocrate
    crate.write(ROCRATE_EXPORT_ROOT)

if __name__ == '__main__':
    main()
