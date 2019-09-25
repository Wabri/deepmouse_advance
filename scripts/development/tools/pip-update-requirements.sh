#!/bin/sh

# Check if root of project are already set
if [ -z "$ROOT" ]; then
	ROOT=$(pwd)
fi

_help(){
	echo 'Usage: ./pip-update-requirements.sh [OPTION]'
	echo ''
	echo 'Mandatory arguments to long options are mandatory for short options too.'
	echo ''
	echo '  -h, --help \t\t\t Print help page'
	echo ''
	echo '  -r, --requirements NAME\t Specify the path to the requirements file'
	echo ''
	echo '  -u, --uninstall NAME\t\t Specify the package to remove'
	echo ''
	echo '  -i, --install NAME\t\t Specify the package to install'
	echo ''
}

_sep_echo(){
	echo '---------------------------'
	echo $1
}

requirements_file=error
requirement=error
is_done=0
error=0
while [ $# -ne 0 ]
do
  key="$1"
  case $key in
    --requirements|-r)
		shift
		requirements_file=$1
		shift
		error=-1
    ;;
	--install|-i)
		shift
		requirement=$1
		shift
		is_done=1
	;;
    --uninstall|-u)
		shift
		requirement=$1
		shift
		is_done=2
    ;;
    --help|-h)
		error=1
		shift
    ;;
	*)
		error=2
		shift
  esac
done

if [ $error -gt 1 ] ;
then
	_sep_echo 'ERROR '$error
	echo 'Need help?'
	echo 'Try using -h or --help arguments'
elif [ $error -eq 1 ] ;
then
	_help
else
	if [ $requirements_file = 'error' ]
	then
		_sep_echo 'ERROR '$error
		echo 'Need help?'
		echo 'Try using -h or --help arguments'
	else
		if [ $is_done -eq 1 ] ; then
			_sep_echo 'Install '$requirement' and update requirement file under '$requirements_file
			is_install=$(pip install $requirement | grep --ignore-case 'Requirement already satisfied: '$requirement)
			if [ -z "$is_install" ]; then
				cp $requirements_file "$requirements_file"_backup
				if [ -z $(cat $requirements_file | grep --ignore-case $requirement) ] ; then
					pip freeze | grep --ignore-case $requirement >> $requirements_file
				fi
			else
				echo 'Requirement already satisfy'
			fi
		elif [ $is_done -eq 2 ] ; then
			_sep_echo 'Uninstall '$requirement' and update requirement file under '$requirements_file
			echo 'Proceed (y/n)?'
			is_uninstall=$(pip uninstall $requirement | grep --ignore-case 'Uninstalling '$requirement)
			if [ ! -z "$is_uninstall" ]; then
				cp $requirements_file "$requirements_file"_backup
				if [ ! -z $(cat $requirements_file | grep --ignore-case $requirement) ] ; then
					delete_line=$(cat $requirements_file | grep --ignore-case $requirement)
					sed -i "/^$delete_line\b/Id" $requirements_file
				fi
			fi
		fi
	fi
fi

_sep_echo ''

