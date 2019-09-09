from glob import glob
import os
import sys
from pymouse import PyMouse
import re
import time
from mouse_recorder.config import config
import signal


def _merge(*, dataset_path, filename_template, files_extension_template, remove_same=False, ordered=True, file_output='output.csv'):
    """
    """
    files_path = dataset_path+'/*.{}'.format(files_extension_template)
    files = glob(files_path)

    if ordered:
        key = lambda x:int(x.lstrip(dataset_path+filename_template).rstrip('.'+files_extension_template))
        files = sorted(glob(files_path), key=key)

    with open(dataset_path + '/' + file_output, 'w') as merge:
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

    with open(dataset_path + '/' + file_output, 'r') as merged:
        print('The merged file lines are: {}'.format(len(merged.readlines())))


def _merge_datas(*, dataset_path, filename_template, files_extension_template, output_file_name, output_extension):
    """
    """
    if os.path.exists(dataset_path):
        print('Dataset path {}/'.format(dataset_path))
        print('With removing same')
        _merge(dataset_path=dataset_path, filename_template=filename_template, files_extension_template=files_extension_template, remove_same=True, ordered=True, file_output='{}.{}'.format(output_file_name, output_extension))
        print('With same')
        _merge(dataset_path=dataset_path, filename_template=filename_template, files_extension_template=files_extension_template, remove_same=False, ordered=True, file_output='{}_ws.{}'.format(output_file_name,output_extension))
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


def _increment_filename(path='.', filename='file', ext='.txt', max_digit=6):
    """
    """
    ext = '.' + ext
    files = glob(os.path.join(path, filename + '*' + ext))
    regex_pattern = '(?<=)(\d+)(?={}$)'.format(ext)
    new_complete_path = ''
    last_file_number = _get_last_number_file(files, regex_pattern)

    if files:
        new_file_number = str(last_file_number + 1)
        new_count = '0' * (max_digit - len(new_file_number)) + new_file_number
        new_complete_path = re.sub(regex_pattern, new_count, files[0])
    else:
        new_complete_path = os.path.join(path, filename + ('0' * max_digit) + ext)

    return new_complete_path


def run_mouse_recorder(*, username, filename_template, files_extension_template, max_iterations, point_per_file, sleep_time):
    """
    """
    if not os.path.exists('./dataset/{}'.format(username)):
        os.makedirs('./dataset/{}'.format(username))
    dataset_path = './dataset/{}/'.format(username)

    mouse = PyMouse()
    run = 0

    while max_iterations < 0 or run < max_iterations:
        print('Recording run {}'.format(run))
        record_filename = _increment_filename(
            path=dataset_path,
            filename=filename_template,
            ext=files_extension_template,
            max_digit=len(str(max_iterations)))
        run += 1
        with open(record_filename, 'w') as rf:
            for index in range(point_per_file):
                x, y = mouse.position()
                rf.write('{},{}\n'.format(x,y))
                time.sleep(sleep_time)
                _progress_bar(index, point_per_file)

        print()

if __name__ == '__main__':

    class params:
        username = 'default'
        max_iterations = config.MAX_ITERATIONS
        point_per_file = config.POINT_PER_FILE
        sleep_time = config.SLEEP_TIME
        filename_template = config.FILENAME_TEMPLATE
        files_extension_template = config.FILES_EXTENSION_TEMPLATE
        dataset_path = config.DATASET_PATH

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

    params.username = str(params.username)
    params.max_iterations = int(params.max_iterations)
    params.point_per_file = int(params.point_per_file)
    params.sleep_time = float(params.sleep_time)
    params.filename_template = str(params.filename_template)
    params.files_extension_template = str(params.files_extension_template)
    params.dataset_path = str(params.dataset_path)

    run_mouse_recorder(
        username=params.username,
        filename_template=params.filename_template,
        files_extension_template=params.files_extension_template,
        max_iterations=params.max_iterations,
        point_per_file=params.point_per_file,
        sleep_time=params.sleep_time
    )

    _merge_datas(
        dataset_path=params.dataset_path+'/{}'.format(params.username),
        filename_template=params.filename_template,
        files_extension_template=params.files_extension_template,
        output_file_name=params.username,
        output_extension='csv'
    )

