import os


def get_test_file_data(filename):
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, filename)
    return open(file_path)
