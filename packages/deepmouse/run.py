import pymouse
import time


def save_mouse_position_to_file(x, y, file):
    with open(file, 'a') as append_file:
        print('Mouse Position: {}, {}'.format(x, y), file=append_file, end='\n')


def load_mouse_position_from_file(file):
    with open(file, 'r') as read_file:
        line = read_file.readlines()[-1]
        print(line, end='')


if __name__ == '__main__':
    while True:
        mouse = pymouse.PyMouse()
        x, y = mouse.position()
        save_mouse_position_to_file(x, y, 'test.txt')
        time.sleep(1)
        load_mouse_position_from_file('test.txt')
