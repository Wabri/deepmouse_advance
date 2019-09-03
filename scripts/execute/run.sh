#!/bin/sh

# Arg 1: name of the package to run
# Arg 2: arguments if necessary

_sep_echo(){
	echo '---------------------------'
	echo $1
}

package_path=packages/$1
environment_path=$package_path/env
main_file=$package_path/$1/run.py

_sep_echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
_sep_echo 'Activate Environment'
. $environment_path/bin/activate
_sep_echo 'Upgrade pip'
pip install --upgrade pip
_sep_echo $separator
_sep_echo 'Intall requirements of mouse_recorder'
pip install -r $package_path/requirements.txt
echo 'Run mouse_recorder with python3 and 2 arguments'
PYTHONPATH=./$package_path python3 $main_file $@
echo 'Deactivate environment'
deactivate
_sep_echo 'Remove environment'
rm -rf $environment_path

_sep_echo ''
