import yaml

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


    def load_yml(self, path):
        ## TODO
        with open(path, 'r') as ymlconfig:
            config = yaml.load(ymlconfig)
        for section in config:
            print(section)

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

