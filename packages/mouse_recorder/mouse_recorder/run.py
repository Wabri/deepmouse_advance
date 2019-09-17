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
from mouse_recorder.terminal.write import *

configuration = Config()
stop = Event()

number_arguments = len(sys.argv) - 2
current_argument = 0

clear_all()
print('Load arguments values')
for arg in sys.argv[2:]:
    title = 'Load argument {}/{}'.format(current_argument + 1, len(sys.argv) - 2)
    couple = str(arg).split(sep='=')
    argument = couple[0].lstrip('--').upper()
    try:
        value = couple[1]
    except:
        value = True

    if argument == 'configuration'.upper():
        clear_all()
        configuration.load_yml(value)
        time.sleep(1)
        break

    configuration.update_argument(argument, value)
    progress_bar(current_argument, number_arguments, title=title)
    current_argument += 1
    time.sleep(1)
clear_all()
print()


def _get_last_number_file(files, regex_pattern):
    """
    """
    last_file_number = 0
    for file in files:
        file_number = int(re.findall(regex_pattern, os.path.basename(file))[0])
        last_file_number = last_file_number if last_file_number >= file_number else file_number
    return last_file_number


def _increment_filename(dataset_path,filename_template,files_extension_template,max_digit):
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


def run_mouse_recorder(username, dataset_path, filename_template, files_extension_template, max_iterations, point_per_file, sleep_time):
    """
    """
    dataset_path = '{}/{}'.format(dataset_path, username)
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    dataset_path = '{}/'.format(dataset_path)

    mouse = PyMouse()
    run = 0

    while (max_iterations < 0 or run < max_iterations) and not stop.is_set():
        title =  'Recording run {}'.format(run)
        record_filename = _increment_filename(
            dataset_path,
            filename_template,
            files_extension_template,
            len(str(max_iterations)) if max_iterations > 0 else 1
        )
        with open(record_filename, 'w') as rf:
            for index in range(point_per_file):
                if stop.is_set():
                    break
                x, y = mouse.position()
                rf.write('{},{}\n'.format(x,y))
                progress_bar(index, point_per_file, title=title)
                stop.wait(sleep_time)
        clear_line()
        title = 'Run {} recorded and save with path {}'.format(run, record_filename)
        print(title)
        run += 1


def _interruption(sig, _frame):
    stop.set()
    clear_all()
    if configuration.MERGE_FILES:
        merge_datas(
            dataset_path='{}/{}'.format(configuration.DATASET_PATH, configuration.USERNAME),
            filename_template=configuration.FILENAME_TEMPLATE,
            files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
            output_file_name=configuration.OUTPUT_FILE_MERGE,
            output_extension=configuration.OUTPUT_EXTENSION
        )
    clear_all()

if __name__ == '__main__':

    if configuration.ONLY_MERGE:
        clear_all()
        merge_datas(
            dataset_path='{}/{}'.format(configuration.DATASET_PATH, configuration.USERNAME),
            filename_template=configuration.FILENAME_TEMPLATE,
            files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
            output_file_name=configuration.OUTPUT_FILE_MERGE,
            output_extension=configuration.OUTPUT_EXTENSION
        )
        clear_all()
        exit()


    signal.signal(signal.SIGINT, _interruption)

    run_mouse_recorder(
        username=configuration.USERNAME,
        dataset_path=configuration.DATASET_PATH,
        filename_template=configuration.FILENAME_TEMPLATE,
        files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
        max_iterations=configuration.MAX_ITERATIONS,
        point_per_file=configuration.POINT_PER_FILE,
        sleep_time=configuration.SLEEP_TIME
    )

    if not stop.is_set():
        os.kill(os.getpid(), signal.SIGINT)

