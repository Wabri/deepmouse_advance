#!/bin/bash

# Check if root of project are already set
if [ -z "$ROOT" ]; then
	ROOT=$(pwd)
fi

_help(){
	echo 'Usage: ./source.sh [OPTION]'
	echo ''
	echo 'Mandatory arguments to long options are mandatory for short options too.'
	echo ''
	echo '  -h, --help \t\t\t Print help page'
	echo ''
	echo '  -p, --package PATH\t\t Specify the path to the package'
	echo ''
	echo '  -m, --main PATH\t\t Specify the path to the main file'
	echo ''
}

_sep_echo(){
	echo '---------------------------'
	echo $1
}

packages_path=$ROOT/packages
main_file=error
is_done=0
error=0
while [ $# -ne 0 ] && [ $is_done -eq 0 ] && [ $error -eq 0 ]
do
  key="$1"
  case $key in
	--main|-m)
		main_file=$2
		shift
		is_done=1
	;;
    --package|-p)
		shift
		main_file=$packages_path/$1/run.py
		is_done=2
    ;;
	*)
		error=1
  esac
done

if [ $error -gt 0 ]
then
	echo 'ERROR '$error
	echo 'Need help?'
	echo 'Try using -h or --help arguments'
else
	if [ $main_file = 'error' ]
	then
		echo 'ERROR '$error
		echo 'Need help?'
		echo 'Try using -h or --help arguments'
	else
		_sep_echo 'Run '$main_file' with args '${@:2}
		PYTHONPATH=$packages_path python $main_file ${@:2}
	fi
fi

_sep_echo ''
