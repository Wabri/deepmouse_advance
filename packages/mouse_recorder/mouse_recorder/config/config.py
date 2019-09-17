import yaml
import os

class Config:

    USERNAME='noname'
    SLEEP_TIME=0.01
    POINT_PER_FILE=100
    MAX_ITERATIONS=5
    FILENAME_TEMPLATE='set_'
    FILES_EXTENSION_TEMPLATE='txt'
    DATASET_PATH='dataset'
    OUTPUT_FILE_MERGE='output'
    OUTPUT_EXTENSION='csv'
    MERGE_FILES=True
    ONLY_MERGE=False

    def __init__(self):
        try:
            load_yml('config.yml')
        except:
            pass


    def load_yml(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as ymlconfig:
                config = yaml.load(ymlconfig)
            for arg in config['mouse_recorder']:
                try:
                    print('Change {} from {}'.format(arg, config['mouse_recorder'][arg]), end='')
                    self.__setattr__(arg,config['mouse_recorder'][arg])
                    print(' to {}'.format(self.__getattribute__(arg)))
                except:
                    print(' but {} argument does not exists'.format(arg))
            self.reset_type()
        else:
            raise FileNotFoundError


    def update_argument(self, argument, value):
        try:
            print('- Change {} from {}'.format(argument, self.__getattribute__(argument)), end='')
            self.__setattr__(argument,value)
            print(' to {}'.format(value))
        except:
            print('- {} argument does not exists'.format(argument))
        self.reset_type()


    def reset_type(self):
        self.USERNAME=str(self.USERNAME)
        self.SLEEP_TIME=float(self.SLEEP_TIME)
        self.POINT_PER_FILE=int(self.POINT_PER_FILE)
        self.MAX_ITERATIONS=int(self.MAX_ITERATIONS)
        self.FILENAME_TEMPLATE=str(self.FILENAME_TEMPLATE)
        self.FILES_EXTENSION_TEMPLATE=str(self.FILES_EXTENSION_TEMPLATE)
        self.DATASET_PATH=str(self.DATASET_PATH)
        self.OUTPUT_FILE_MERGE=str(self.OUTPUT_FILE_MERGE)
        self.OUTPUT_EXTENSION=str(self.OUTPUT_EXTENSION)

