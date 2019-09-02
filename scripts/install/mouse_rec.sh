#!/bin/sh

_sep_echo(){
	echo '---------------------------'
	echo $1
}

package_path=packages/mouse_recorder
environment_path=$package_path/env

_sep_echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
_sep_echo $separator
_sep_echo 'Activate environment'
. $environment_path/bin/activate
_sep_echo $separator
_sep_echo 'Upgrade pip'
pip install --upgrade pip
_sep_echo $separator
_sep_echo 'Install requirements of mouse_recorder'
pip install -r $package_path/requirements.txt
_sep_echo $separator
_sep_echo 'Install pyinstaller'
pip install pyinstaller
_sep_echo $separator
_sep_echo 'Remove Useless files and folders'
rm -rf build dist
_sep_echo $separator
_sep_echo 'Create mouse_rec executable'
pyinstaller --onefile $package_path/mouse_rec.spec
_sep_echo $separator
_sep_echo 'Deactivate virtual environment'
deactivate
_sep_echo $separator
_sep_echo 'Remove environment'
rm -rf $environment_path
_sep_echo $separator
_sep_echo 'Remove build and move executable'
rm -rf mouse_rec.run
mv dist/mouse_rec ./mouse_rec.run
rm -rf build dist

_sep_echo $separator

