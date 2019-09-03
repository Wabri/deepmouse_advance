from glob import glob
import os
import sys
from pymouse import PyMouse
import re
import time
from mouse_recorder.config import config


def _progress_bar(current_value, max_value):
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


def run_mouse_recorder(*, username, max_iterations, point_per_file, sleep_time):
    """
    """
    if not os.path.exists('./dataset/{}'.format(username)):
        os.makedirs('./dataset/{}'.format(username))
    dataset_path = './dataset/{}/'.format(username)

    mouse = PyMouse()
    run = 0

    N = point_per_file

    while max_iterations < 0 or run < max_iterations:
        print('Recording run {}'.format(run))
        record_filename = _increment_filename(path=dataset_path, max_digit=len(str(max_iterations)))
        run += 1

        with open(record_filename, 'w') as rf:
            for index in range(N):
                x, y = mouse.position()
                rf.write('{},{}'.format(x,y))
                time.sleep(sleep_time)
                _progress_bar(index, N)

        print()

if __name__ == '__main__':

    class params:
        username = 'default'
        max_iterations = config.MAX_ITERATIONS
        point_per_file = config.POINT_PER_FILE
        sleep_time = config.SLEEP_TIME

    for arg in sys.argv[1:]:
        arguments = str(arg).split(sep='=')
        try:
            argument = arguments[0].lstrip('--')
            try:
                value = arguments[1]
            except:
                value = True
            if getattr(params, argument):
                setattr(params, argument, value)
            else:
                print("Argument {} don't have references".format(argument))
        except Exception as e:
            pass

    run_mouse_recorder(
        username=str(params.username),
        max_iterations=int(params.max_iterations),
        point_per_file=int(params.point_per_file),
        sleep_time=int(params.sleep_time)
    )

