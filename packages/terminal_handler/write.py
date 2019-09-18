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


def progress_bar(current_value, max_value, padding=0, title='', leave_title=False):
    """
    """
    clear_line()
    columns = os.get_terminal_size().columns
    total_padding = padding + 11
    bar_spaces = columns - total_padding
    absolute_progress = ((current_value + 1)/max_value) * 100
    progress = absolute_progress / 100 * bar_spaces
    bar = '[{}{}] {:3.0f}%'.format('#'*int(progress + (0 if not absolute_progress == 100 else -1)), ' '*int(bar_spaces - progress), absolute_progress)
    output = title + '\n' + bar
    print(output)
    move_up() if leave_title and not absolute_progress == 100 else move_up(2)
    print('') if absolute_progress == 100 else print('', end='\r')
    #print(title)
    #columns = os.get_terminal_size().columns
    #progress = ((current_value + 1) / max_value) * columns
    #clear_line()
    #bar = '[{0}{1}] {2:.1f}%'.format('#'*int(progress/2), ' ' * (columns/2-int(progress/2)), progress)
    #output_string = ((title + '\n') if not title == '' else '')  + bar
    #print(output_string, end='')
    #if not title == '': move_up()
    #print('', end='\r')
    #if leave_title:
    #    print(title)

if __name__ == '__main__':
    import time
    for i in range(100):
        progress_bar(i, 100, padding=150, title='Yolo {}'.format(i), leave_title=False)
        time.sleep(0.01)

