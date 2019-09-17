import os

def move_up(times=1):
    for _ in range(times):
        print('',end='\x1b[A')


def move_down(times=1):
    for _ in range(times):
        print('',end='\x1b[B')


def clear_line(end='\r'):
    characters = os.get_terminal_size().columns
    print(' '*characters, end=end)


def clear_lines(lines):
    for _ in range(lines):
        clear_line(end='\r')
        move_up()


def clear_all():
    lines = os.get_terminal_size().lines
    move_down()
    clear_lines(lines)


def progress_bar(current_value, max_value, title='', leave_title=False):
    """
    """
    progress = ((current_value + 1) / max_value) * 100
    if progress > 98:
        progress = 100
    clear_line()
    bar = '[{0}{1}] {2:.1f}%'.format('#'*int(progress/2), ' ' * (50-int(progress/2)), progress)
    output_string = ((title + '\n') if not title == '' else '')  + bar
    print(output_string, end='')
    if not title == '': move_up()
    print('', end='\r')
    if leave_title:
        print(title)


