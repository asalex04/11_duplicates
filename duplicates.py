import os
import hashlib
import argparse
import collections


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
         help='path to root directory'
    )
    return parser


def get_duplicates(dir_path):
    filenames_with_pathes_dict = collections.defaultdict(list)
    for root, dirs, file_names in os.walk(dir_path):
        for filename in file_names:
            fullpath = os.path.join(root, filename)
            file_hash = get_file_hash_md5(fullpath)
            filenames_with_pathes_dict[file_hash].append(fullpath)
    return filenames_with_pathes_dict


def get_file_hash_md5(file_for_hash):
    hasher = hashlib.md5()
    blocksize = 1024 * 1024
    with open(file_for_hash, 'rb') as file:
        buff = file.read(blocksize)
        hasher.update(buff)
    return hasher.hexdigest()


def print_path_duplicate_file(files_duplicates):
    print('Scanning... {}'.format(files_duplicates))
    for _, list_of_duplicates in files_hash_and_path_dict.items():
        if len(list_of_duplicates) > 1:
            print('\nDuplicates:')
            print('\n'.join(list_of_duplicates))


if __name__ == '__main__':
    parser = get_parser()
    list_of_filepaths = parser.parse_args().path

    if os.path.isdir(list_of_filepaths):
        files_hash_and_path_dict = get_duplicates(list_of_filepaths)
        if files_hash_and_path_dict:
            print_path_duplicate_file(list_of_filepaths)
        else:
            print('Nothing found in {}'.format(list_of_filepaths))
    else:
        print('Enter existing directory')
