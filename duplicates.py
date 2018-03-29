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


def get_duplicates(search_dir_path):
    files_with_pathes_dict = collections.defaultdict(list)
    for root, dirs, files in os.walk(search_dir_path):
        for filename in files:
            fullpath = os.path.join(root, filename)
            file_hash = get_file_hash_md5(fullpath)
            files_with_pathes_dict[file_hash].append(fullpath)
    return files_with_pathes_dict


def get_file_hash_md5(file_for_hash, blocksize=4096):
    hasher = hashlib.md5()
    with open(file_for_hash, 'rb') as file:
        while True:
            buff = file.read(blocksize)
            if not buff:
                break
            hasher.update(buff)
        return hasher.hexdigest()


def print_path_duplicate_file(print_dir_path):
    print('Scanning... {}'.format(print_dir_path))
    for _, list_of_filepaths in files_hash_and_path_dict.items():
        if len(list_of_filepaths) > 1:
            print('\nDuplicates:')
            for filepath in list_of_filepaths:
                print(filepath)


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
