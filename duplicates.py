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
    for root, dirs, files in os.walk(dir_path):
        for filename in files:
            fullpath = os.path.join(root, filename)
            file_hash = get_file_hash_md5(fullpath)
            filenames_with_pathes_dict[file_hash].append(fullpath)
    return files_with_pathes_dict


def get_file_hash_md5(file_for_hash, first_block=False):
    hasher = hashlib.md5()
    blocksize = 1024 * 1024
    file_size = os.path.getsize(file_for_hash)
    with open(file_for_hash, 'rb') as file:
        while True:
            buff = file.read(blocksize)
            hasher.update(buff)
            file_size -= blocksize
            if (len(buff) < blocksize or first_block):
                break
        return hasher.hexdigest()


def print_path_duplicate_file(print_dir_path):
    print('Scanning... {}'.format(print_dir_path))
    for _, list_of_filepaths in files_hash_and_path_dict.items():
        if len(list_of_filepaths) > 1:
            print('\nDuplicates:')
            print('\n'.join(list_of_filepaths))


if __name__ == '__main__':
    parser = get_parser()
    search_dir_path = parser.parse_args().path

    if os.path.isdir(search_dir_path):
        files_hash_and_path_dict = get_duplicates(search_dir_path)
        if files_hash_and_path_dict:
            print_path_duplicate_file(search_dir_path)
        else:
            print('Nothing found in {}'.format(search_dir_path))
    else:
        print('Enter existing directory')
