from glob import glob
import os
import sys
from pymouse import PyMouse
import re
from threading import Event
from mouse_recorder.config.config import Config
import signal
import time

configuration = Config()
stop = Event()

for arg in sys.argv[2:]:
    arguments = str(arg).split(sep='=')
    print(arguments)
    argument = arguments[0].lstrip('--').upper()
    try:
        value = arguments[1]
    except:
        value = True
    if hasattr(configuration, argument):
        print('Change {} from {}'.format(argument, getattr(configuration, argument)),end=' ')
        setattr(configuration, argument, value)
        print('to {}'.format(getattr(configuration, argument)))
    else:
        print("Argument {} don't have references".format(argument))
configuration.reset_type()


def _merge(
        username=configuration.USERNAME,
        dataset_path=configuration.DATASET_PATH,
        filename_template=configuration.FILENAME_TEMPLATE,
        files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
        remove_same=True,
        ordered=True,
        file_output=configuration.USERNAME):
    """
    """
    files = glob('{}/*'.format(dataset_path))

    if ordered:
        key = lambda x:int(x.split('/')[-1].rstrip('.{}'.format(files_extension_template)).lstrip('{}'.format(filename_template)))
        files = sorted(glob('{}/{}/*'.format(dataset_path,username)), key=key)

    with open(file_output, 'w') as merge:
        last_line = ''
        for file in files:
            with open(file,'r') as dataset:
                for line in dataset.readlines():
                    if remove_same:
                        if last_line != line:
                            merge.write('{}'.format(line))
                        last_line = line
                    else:
                        merge.write('{}'.format(line))

    with open(file_output, 'r') as merged:
        print('The merged file lines are: {}'.format(len(merged.readlines())))


def _merge_datas(
        username=configuration.USERNAME,
        dataset_path=configuration.DATASET_PATH,
        filename_template=configuration.FILENAME_TEMPLATE,
        files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
        output_file_name=configuration.USERNAME,
        output_extension=configuration.FILES_EXTENSION_TEMPLATE,
        sleep_time=configuration.SLEEP_TIME):
    """
    """
    time.sleep(sleep_time)
    if os.path.exists(dataset_path):
        print('Dataset path {}/'.format(dataset_path))
        print('With removing same and work with ordered')
        _merge(
            username=username,
            dataset_path=dataset_path,
            filename_template=filename_template,
            files_extension_template=files_extension_template,
            remove_same=True,
            ordered=True,
            file_output='{}.{}'.format(output_file_name,output_extension)
        )
        print('With same and work with ordered')
        _merge(
            username=username,
            dataset_path=dataset_path,
            filename_template=filename_template,
            files_extension_template=files_extension_template,
            remove_same=False,
            ordered=True,
            file_output='{}_withsame.{}'.format(output_file_name,output_extension)
        )
    else:
        print('The path does not exist')


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


def _increment_filename(
        dataset_path='{}/{}'.format(configuration.DATASET_PATH,configuration.USERNAME),
        filename_template=configuration.FILENAME_TEMPLATE,
        files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
        max_digit=len(str(configuration.MAX_ITERATIONS))):
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
        username=configuration.USERNAME,
        dataset_path=configuration.DATASET_PATH,
        filename_template=configuration.FILENAME_TEMPLATE,
        files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
        max_iterations=configuration.MAX_ITERATIONS,
        point_per_file=configuration.POINT_PER_FILE,
        sleep_time=configuration.SLEEP_TIME):
    """
    """
    dataset_path = '{}/{}'.format(dataset_path, username)
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    dataset_path = '{}/'.format(dataset_path)

    mouse = PyMouse()
    run = 0

    while (max_iterations < 0 or run < max_iterations) and not stop.is_set():
        print('Recording run {}'.format(run))
        record_filename = _increment_filename(
            dataset_path,
            filename_template,
            files_extension_template,
            len(str(max_iterations))
        )
        run += 1
        with open(record_filename, 'w') as rf:
            for index in range(point_per_file):
                if stop.is_set():
                    break
                x, y = mouse.position()
                rf.write('{},{}\n'.format(x,y))
                _progress_bar(index, point_per_file)
                stop.wait(sleep_time)
        print()


def interruption(sig, _frame):
    stop.set()
    if configuration.MERGE_FILES:
        _merge_datas(
            configuration.USERNAME,
            configuration.DATASET_PATH,
            configuration.FILENAME_TEMPLATE,
            configuration.FILES_EXTENSION_TEMPLATE,
            configuration.OUTPUT_FILE_MERGE,
            configuration.OUTPUT_EXTENSION,
            configuration.SLEEP_TIME
        )

if __name__ == '__main__':

    if configuration.ONLY_MERGE:
        _merge_datas(
            username=configuration.USERNAME,
            dataset_path=configuration.DATASET_PATH,
            filename_template=configuration.FILENAME_TEMPLATE,
            files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
            output_file_name=configuration.OUTPUT_FILE_MERGE,
            output_extension=configuration.OUTPUT_EXTENSION,
            sleep_time=configuration.SLEEP_TIME
        )
        exit()

    for file in glob(configuration.DATASET_PATH+'/*'):
        try:
            files_extension_template = '.' + configuration.FILES_EXTENSION_TEMPLATE
            files = glob(os.path.join(configuration.DATASET_PATH, configuration.FILENAME_TEMPLATE + '*.' + configuration.FILES_EXTENSION_TEMPLATE))
            for file in files:
                print(int(file.lstrip('{}/{}'.format(configuration.DATASET_PATH,configuration.FILENAME_TEMPLATE)).rstrip('.'+configuration.FILES_EXTENSION_TEMPLATE)))
        except:
            print(file)

    signal.signal(signal.SIGINT, interruption)

    run_mouse_recorder(
        username=configuration.USERNAME,
        filename_template=configuration.FILENAME_TEMPLATE,
        files_extension_template=configuration.FILES_EXTENSION_TEMPLATE,
        max_iterations=configuration.MAX_ITERATIONS,
        point_per_file=configuration.POINT_PER_FILE,
        sleep_time=configuration.SLEEP_TIME
    )

    if not stop.is_set():
        os.kill(os.getpid(), signal.SIGINT)

