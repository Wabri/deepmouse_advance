from glob import glob
from mouse_recorder.config.config import Config
from terminal_handler.write import *

config = Config()

def _merge(dataset_path, filename_template, files_extension_template, remove_same, ordered, file_output):
    """
    """
    files_path = '{}/*.{}'.format(dataset_path, files_extension_template)
    files = glob(files_path)

    if ordered:
        key = lambda x:int(x.lstrip('{}/{}'.format(dataset_path,filename_template)).rstrip('.'+files_extension_template))
        files = sorted(glob(files_path), key=key)

    with open('{}.{}'.format(file_output, files_extension_template), 'w') as merge:
        last_line = ''
        number_file = 0
        number_files = len(files)
        merge_lines = 0

        for file in files:
            current_merge_lines = 0
            lines_number = 0
            with open(file,'r') as dataset:
                lines = dataset.readlines()
                title = 'File {}/{}'.format(number_file + 1, number_files)
                current_line = 0
                lines_number = len(lines)

                for line in lines:
                    if remove_same:
                        if last_line != line:
                            merge.write('{}'.format(line))
                            merge_lines += 1
                            current_merge_lines += 1
                        last_line = line
                    else:
                        merge.write('{}'.format(line))
                        merge_lines += 1
                        current_merge_lines += 1
                    progress_bar(current_line, lines_number, title=title)
                    current_line += 1

                clear_line()
                print('{}: {} lines into {} '.format(title, lines_number, current_merge_lines))
                number_file += 1
        clear_line()

    print('Total lines merged: {}'.format(merge_lines))


def merge_datas(*,
        dataset_path='{}/{}'.format(config.DATASET_PATH, config.USERNAME),
        filename_template=config.FILENAME_TEMPLATE,
        files_extension_template=config.FILES_EXTENSION_TEMPLATE,
        output_file_name=config.USERNAME,
        output_extension=config.FILES_EXTENSION_TEMPLATE):
    """
    """

    if os.path.exists(dataset_path):
        print('Dataset path {}/'.format(dataset_path))
        print('Merge removing same')
        _merge(dataset_path=dataset_path, filename_template=filename_template, files_extension_template=files_extension_template, remove_same=True, ordered=True, file_output='{}'.format(output_file_name, output_extension))
        print('Merge with same')
        _merge(dataset_path=dataset_path, filename_template=filename_template, files_extension_template=files_extension_template, remove_same=False, ordered=True, file_output='{}_ws'.format(output_file_name,output_extension))
    else:
        print('The path does not exist')
