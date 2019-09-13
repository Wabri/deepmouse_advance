import time
import glob

def _merge(
        dataset_path='{}/{}'.format(config.DATASET_PATH, config.USERNAME),
        filename_template=config.FILENAME_TEMPLATE,
        files_extension_template=config.FILES_EXTENSION_TEMPLATE,
        remove_same=config.REMOVE_SAME,
        ordered=True,
        file_output=config.USERNAME):
    """
    """
    files_path = '{}/*.{}'.format(dataset_path, files_extension_template)
    files = glob(files_path)

    if ordered:
        key = lambda x:int(x.lstrip('{}/{}'.format(dataset_path,filename_template)).rstrip('.'+files_extension_template))
        files = sorted(glob(files_path), key=key)

    with open('{}.{}'.format(file_output, files_extension_template), 'w') as merge:
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

    with open('{}.{}'.format(file_output, files_extension_template), 'r') as merged:
        print('The merged file lines are: {}'.format(len(merged.readlines())))


def merge_datas(
        dataset_path='{}/{}'.format(config.DATASET_PATH, config.USERNAME),
        filename_template=config.FILENAME_TEMPLATE,
        files_extension_template=config.FILES_EXTENSION_TEMPLATE,
        output_file_name=config.USERNAME,
        output_extension=config.FILES_EXTENSION_TEMPLATE,
        sleep_time=config.SLEEP_TIME):
    """
    """
    time.sleep(sleep_time)
    if os.path.exists(dataset_path):
        print('Dataset path {}/'.format(dataset_path))
        print('With removing same')
        _merge(dataset_path=dataset_path, filename_template=filename_template, files_extension_template=files_extension_template, remove_same=True, ordered=True, file_output='{}'.format(output_file_name, output_extension))
        print('With same')
        _merge(dataset_path=dataset_path, filename_template=filename_template, files_extension_template=files_extension_template, remove_same=False, ordered=True, file_output='{}_ws'.format(output_file_name,output_extension))
    else:
        print('The path does not exist')
