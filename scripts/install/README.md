
# Install

# On linux

To use this script you must abilitate the source [file](/scripts/development_setup).

The script [install.sh](install.sh): Set up the virtual environment and activate it, install pip and requirements, install pyinstaller, run pyinstaller with the spec of the package passed in argument, deactivate and remove environment, move the executable to root folder and remove build and dist directories.

To use it is necessary to specificate what package run and the name of the file in output:

```Bash
sh scripts/install/install.sh <name_of_package> <output_file_name>
```

The execution of this script create a *.run*.

## Mouse recorder

Example:

```Bash
sh scripts/install/install.sh mouse_recorder mouse_recorder_executable
```

The output file would be *mouse_recorder_executable.run*.

