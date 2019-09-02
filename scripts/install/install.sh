#!/bin/sh

# Arg 1: name of the package to install
# Arg 2: name of the output file

_sep_echo(){
	echo '---------------------------'
	echo $1
}

package_path=packages/$1
environment_path=$package_path/env
spec_file=$package_path/$1.spec

_sep_echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
_sep_echo 'Activate environment'
. $environment_path/bin/activate
_sep_echo 'Upgrade pip'
pip install --upgrade pip
_sep_echo 'Install requirements of mouse_recorder'
pip install -r $package_path/requirements.txt
_sep_echo 'Install pyinstaller'
pip install pyinstaller
_sep_echo 'Remove Useless files and folders'
rm -rf build dist
_sep_echo 'Create mouse_rec executable'
pyinstaller --onefile $package_path/mouse_rec.spec
_sep_echo 'Deactivate virtual environment'
deactivate
_sep_echo 'Remove environment'
rm -rf $environment_path
echo 'Remove build and move executable'
rm -rf $2.run
mv dist/$1 ./$2.run
rm -rf build dist

_sep_echo

