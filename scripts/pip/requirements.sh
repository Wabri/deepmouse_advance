#!/bin/sh

_sep_echo(){
	echo '---------------------------'
	echo $1
}

package_path=packages/$1
environment_path=packages/$1/env
requirements_file_name=$package_path/requirements.txt

_sep_echo 'Deactivate precedent (if exists) environment'
deactivate
_sep_echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
_sep_echo 'Activate Environment'
source $environment_path/bin/activate
_sep_echo 'Upgrade pip'
pip install --upgrade pip
_sep_echo 'Install requirements of package '$1
pip install $2
_sep_echo 'Freeze requirements'
pip freeze > $requirements_file_name
_sep_echo 'Remove first line of freeze'
sed 1d $requirements_file_name > $package_path/temp
_sep_echo 'Move requirements into '$package_path
mv $package_path/temp $requirements_file_name

_sep_echo ''

