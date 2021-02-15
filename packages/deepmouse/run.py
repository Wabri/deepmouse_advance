import pymouse
import time


def save_mouse_position_to_file(x, y, file):
    with open(file, 'a') as append_file:
        print('{}, {}'.format(x, y), file=append_file, end='\n')


def load_mouse_position_from_file(file):
    with open(file, 'r') as read_file:
        line = read_file.readlines()[-1]
        print(line, end='')


if __name__ == '__main__':
    while True:
        file_name = 'test.csv'
        mouse = pymouse.PyMouse()
        x, y = mouse.position()
        save_mouse_position_to_file(x, y, file_name)
        time.sleep(1)
        load_mouse_position_from_file(file_name)
        time.sleep(1)
