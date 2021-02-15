from terminal_handler.write import progress_bar

if __name__ == '__main__':
    import time
    for i in range(10):
        progress_bar(i, 10, title='Yolo {}'.format(i), leave_title=False)
        time.sleep(0.05)
    time.sleep(1)
    for i in range(10):
        progress_bar(i, 10, title='Yolo {}'.format(i), leave_title=True)
        time.sleep(0.05)
    time.sleep(1)
    for i in range(10):
        progress_bar(i, 10, lenght=50, title='Yolo {}'.format(i), leave_title=False)
        time.sleep(0.05)
    time.sleep(1)
    for i in range(10):
        progress_bar(i, 10, lenght=50, padding=20, title='Yolo {}'.format(i), leave_title=False)
        time.sleep(0.05)
    time.sleep(1)

