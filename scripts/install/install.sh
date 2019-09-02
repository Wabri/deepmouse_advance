#!/bin/sh

# Arg 1: name of the package to install
# Arg 2: name of the output file

separator=-------------------------

package_path=packages/$1
environment_path=$package_path/env
spec_file=$package_path/$1.spec

echo $separator
echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
echo $separator
echo 'Activate environment'
. $environment_path/bin/activate
echo $separator
echo 'Upgrade pip'
pip install --upgrade pip
echo $separator
echo 'Install requirements of mouse_recorder'
pip install -r $package_path/requirements.txt
echo $separator
echo 'Install pyinstaller'
pip install pyinstaller
echo $separator
echo 'Remove Useless files and folders'
rm -rf build dist
echo $separator
echo 'Create mouse_rec executable'
pyinstaller --onefile $spec_file
echo $separator
echo 'Deactivate virtual environment'
deactivate
echo $separator
echo 'Remove environment'
rm -rf $environment_path
echo $separator
echo 'Remove build and move executable'
rm -rf $2.run
mv dist/$1 ./$2.run
rm -rf build dist

echo $separator

