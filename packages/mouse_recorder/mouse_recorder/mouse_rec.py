from glob import glob
import os
import sys
from pymouse import PyMouse
import re
import time


def progress_bar(current_value, max_value):
    """
    """
    progress = ((current_value + 1) / max_value) * 100
    if progress > 98:
        progress = 100
    print('\r[{0}{1}] {2:.1f}%'.format('#'*int(progress/2), ' ' * (50-int(progress/2)), progress), end='')


def _get_last_number_file(files, regex_pattern):
    """
    """
    last_file_number = 0
    for file in files:
        file_number = int(re.findall(regex_pattern, os.path.basename(file))[0])
        last_file_number = last_file_number if last_file_number >= file_number else file_number
    return last_file_number

def _increment_filename(path='.', filename='file', ext='txt', max_digit=6):
    """
    """
    files = glob(os.path.join(path, filename + '_*' + ext))
    regex_pattern = '(?<=)(\d+)(?=\.{}$)'.format(ext)
    new_complete_path = ''
    ext = '.' + ext
    last_file_number = _get_last_number_file(files, regex_pattern)

    if files:
        new_file_number = str(last_file_number + 1)
        new_count = '0' * (max_digit - len(new_file_number)) + new_file_number
        new_complete_path = re.sub(regex_pattern, new_count, files[0])
    else:
        new_complete_path = os.path.join(path, filename + '_' + ('0' * max_digit) + ext)

    return new_complete_path


def run_mouse_recorder(username='Default', username_dataset=False):
    """
    """
    filename_template = 'record_{}'.format(username)
    if username_dataset:
        if not os.path.exists('./dataset/{}'.format(username)):
            os.makedirs('./dataset/{}'.format(username))
        dataset_path = './dataset/{}/'.format(username)
    else:
        if not os.path.exists('./dataset'):
            os.makedirs('./dataset')
        dataset_path = './dataset/'
    mouse = PyMouse()
    run = 0
    N = 10
    while True:
        print('Recording run {}'.format(run))
        record_filename = _increment_filename(path=dataset_path, filename=filename_template, max_digit=4)
        run += 1

        with open(record_filename, 'w') as rf:
            for index in range(N):
                x, y = mouse.position()
                rf.write('{},{}'.format(x,y))
                time.sleep(0.01)
                progress_bar(index, N)

        print()

if __name__ == '__main__':
    run_mouse_recorder(username=sys.argv[1], username_dataset=False)
