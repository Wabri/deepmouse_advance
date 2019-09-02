#!/bin/sh

separator=-------------------------

package_path=packages/$1
environment_path=$package_path/env
main_file=$package_path/$1/run.py

echo $separator
echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
echo $separator
echo 'Activate Environment'
. $environment_path/bin/activate
echo $separator
echo 'Upgrade pip'
pip install --upgrade pip
echo $separator
echo 'Intall requirements of mouse_recorder'
pip install -r $package_path/requirements.txt
echo $separator
echo 'Run mouse_recorder with python3 and 2 arguments'
PYTHONPATH=./$package_path python3 $main_file $2 $3
echo $separator
echo 'Deactivate environment'
deactivate
echo $separator
echo 'Remove environment'
rm -rf $environment_path

echo $separator

