#!/bin/sh

separator=-------------------------

environment_path=./venv
scripts_path=./scripts

echo $separator
echo 'Deactivate precedent environment'
deactivate
echo $separator
echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
echo $separator
echo 'Activate Environment'
source $environment_path/bin/activate
echo $separator
echo 'Upgrade pip'
pip install --upgrade pip
echo $separator
echo 'Intall requirements of mouse_recorder'
pip install -r ./requirements.txt

alias run='sh $scripts_path/execute/run.sh'
alias make_exe='sh $scripts_path/install/install.sh'

echo ''
