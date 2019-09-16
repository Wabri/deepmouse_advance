# Mouse_recorder package

The main pourpose of this pack is to gather the mouse position over time.

By default, every milliseconds will be take the position of the mouse and save into a file inside the relative dataset directory.


## Development

The package is divided in one script called run.py that have two main duty: the first one is to run the process of mouse record, and the second one is merge the file of a dataset into a single file.

The merge process it can be done in 3 cases:

1. When the mouse recorder finish the loop
2. When the mouse recorder has stop by an interrupt
3. If the only merge flag has invoke



