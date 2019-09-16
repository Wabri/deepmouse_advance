#!/bin/sh

_sep_echo(){
	echo '---------------------------'
	echo $1
}

root_project=$(pwd)
packages_path=$1
environment_path=$packages_path/venv
scripts_path=$root_project/scripts

_sep_echo 'Install python3 venv dependencies'
sudo apt install python3-venv
_sep_echo 'Install pip3 dependencies'
sudo apt install python3-pip
_sep_echo 'Deactivate precedent environment'
deactivate
_sep_echo 'Setting up virtual environment'
rm -rf $environment_path
python3 -m venv $environment_path
_sep_echo 'Activate Environment'
source $environment_path/bin/activate
_sep_echo 'Upgrade pip'
pip install --upgrade pip
_sep_echo 'Install requirements of mouse_recorder'

pip install -r ./requirements.txt

_sep_echo 'Setting up alias command'
_sep_echo 'You can use the run command to execute python packages run.py'
echo '          run <name_package> [<arguments>]'
alias run='cd $root_project ; sh $scripts_path/execute/run.sh'
_sep_echo 'You can use the make_exe command to create an executable file with pyinstaller'
echo '          make_exe <name_package>'
echo 'The new file will be created in the root folder'
alias make_exe='cd $root_project ; sh $scripts_path/install/install.sh'
_sep_echo 'You can use the requirements command to create a requirements.txt of the package'
echo '          requirements <name_package>'
echo 'The new file will be created in the package folder'
alias requirements='cd $root_project ; sh $scripts_path/pip/requirements.sh'

_sep_echo ''
