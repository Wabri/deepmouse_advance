#!/bin/sh

_sep_echo(){
	echo '---------------------------'
	echo $1
}

package_path=packages/mouse_recorder
requirements_file_name=$package_path/requirements.txt

_sep_echo 'Freeze requirements'
pip freeze > $requirements_file_name
_sep_echo 'Remove first line of freeze'
sed 1d $requirements_file_name > $package_path/temp
mv $package_path/temp $requirements_file_name
_sep_echo

