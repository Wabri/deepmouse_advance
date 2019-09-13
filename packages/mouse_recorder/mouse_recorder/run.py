from glob import glob
import os
import sys
from pymouse import PyMouse
import re
from threading import Event
import signal
import time

from mouse_recorder.config.config import Config
from mouse_recorder.merge.merge_dataset import merge_datas
from mouse_recorder.progress import bar

config = Config()
stop = Event()

for arg in sys.argv[1:]:
    arguments = str(arg).split(sep='=')
    try:
        argument = arguments[0].lstrip('--').upper()
        try:
            value = arguments[1]
        except:
            value = True
        if getattr(config, argument):
            setattr(config, argument, value)
        else:
            print("Argument {} don't have references".format(argument))
    except Exception as e:
        pass


def _get_last_number_file(files, regex_pattern):
    """
    """
    last_file_number = 0
    for file in files:
        file_number = int(re.findall(regex_pattern, os.path.basename(file))[0])
        last_file_number = last_file_number if last_file_number >= file_number else file_number
    return last_file_number


def _increment_filename(
        dataset_path='{}/{}'.format(config.DATASET_PATH,config.USERNAME),
        filename_template=config.FILENAME_TEMPLATE,
        files_extension_template=config.FILES_EXTENSION_TEMPLATE,
        max_digit=len(str(config.MAX_ITERATIONS))):
    """
    """
    files_extension_template = '.' + files_extension_template
    files = glob(os.path.join(dataset_path, filename_template + '*' + files_extension_template))
    regex_pattern = '(?<=)(\d+)(?={}$)'.format(files_extension_template)
    new_complete_path = ''
    last_file_number = _get_last_number_file(files, regex_pattern)

    if files:
        new_file_number = str(last_file_number + 1)
        new_count = '0' * (max_digit - len(new_file_number)) + new_file_number
        new_complete_path = re.sub(regex_pattern, new_count, files[0])
    else:
        new_complete_path = os.path.join(dataset_path, filename_template + ('0' * max_digit) + files_extension_template)

    return new_complete_path


def run_mouse_recorder(
        username=config.USERNAME,
        filename_template=config.FILENAME_TEMPLATE,
        files_extension_template=config.FILES_EXTENSION_TEMPLATE,
        max_iterations=config.MAX_ITERATIONS,
        point_per_file=config.POINT_PER_FILE,
        sleep_time=config.SLEEP_TIME):
    """
    """
    if not os.path.exists('./dataset/{}'.format(username)):
        os.makedirs('./dataset/{}'.format(username))
    dataset_path = './dataset/{}/'.format(username)

    mouse = PyMouse()
    run = 0

    while (max_iterations < 0 or run < max_iterations) and not stop.is_set():
        print('Recording run {}'.format(run))
        record_filename = _increment_filename()
        run += 1
        with open(record_filename, 'w') as rf:
            for index in range(point_per_file):
                if stop.is_set():
                    break
                x, y = mouse.position()
                rf.write('{},{}\n'.format(x,y))
                bar.output(index, point_per_file)
                stop.wait(sleep_time)
        print()


def _interruption(sig, _frame):
    stop.set()
    if config.MERGE_FILES:
        merge_datas(
            dataset_path='{}/{}'.format(config.DATASET_PATH, config.USERNAME),
            filename_template=config.FILENAME_TEMPLATE,
            files_extension_template=config.FILES_EXTENSION_TEMPLATE,
            output_file_name=config.USERNAME,
            output_extension=config.FILES_EXTENSION_TEMPLATE
        )

if __name__ == '__main__':

    signal.signal(signal.SIGINT, _interruption)

    run_mouse_recorder()

    if not stop.is_set():
        os.kill(os.getpid(), signal.SIGINT)

