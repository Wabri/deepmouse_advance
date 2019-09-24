import yaml
import os


class Config:

    COLORS = ['#0c6575',
              '#bbcbcb',
              '#23a98c',
              '#fc7a70',
              '#a07060',
              '#003847',
              '#FFF7D6',
              '#5CA4B5',
              '#eeeeee']

    def __init__(self):
        try:
            self.load_yml('config.yml')
        except:
            pass

    def load_yml(self, config_path):
        if os.path.exists(config_path):
            with open(config_path, 'r') as ymlconfig:
                config = yaml.load(ymlconfig, Loader=yaml.Loader)
            for arg in config['mouse_recognition']:
                try:
                    print('Change {} from {}'.format(arg, self.__getattribute__(arg.upper())), end='')
                    self.__setattr__(arg.upper(), config['mouse_recognition'][arg])
                    print(' to {}'.format(self.__getattribute__(arg.upper())))
                except:
                    print(' but {} argument does not exists'.format(arg))
        else:
            raise FileNotFoundError

    def update_argument(self, argument, value):
        try:
            print('- Change {} from {}'.format(argument, self.__getattribute__(argument)), end='')
            self.__setattr__(argument, value)
            print(' to {}'.format(value))
        except:
            print('- {} argument does not exists'.format(argument))
