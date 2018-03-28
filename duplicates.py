import os
import hashlib
import argparse
import collections


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        type=str,
        help='path to root directory'
    )
    return parser


def get_duplicates(search_dir_path):
    files_with_pathes_dict = collections.defaultdict(list)
    for root, dirs, files in os.walk(search_dir_path):
        for filename in files:
            fullname = os.path.join(root, filename)
            file_hash = get_file_hash_md5(fullname)
            files_with_pathes_dict[file_hash].append(fullname)
    return files_with_pathes_dict


def get_file_hash_md5(duplicates):
    m = hashlib.md5()
    with open(duplicates, 'rb', 4096) as file:
        while True:
            data = file.read(4096)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def print_path_duplicate_file(search_dir_path):
    print('Scanning... {}'.format(search_dir_path))
    for file_hash, list_of_filepaths in files_hash_and_path_dict.items():
        if len(list_of_filepaths) > 1:
            print('\nDuplicates:')
            for filepath in list_of_filepaths:
                print(filepath)
    return


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
