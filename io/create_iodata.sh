#/bin/bash

module load anaconda3

read -r -p "Will create data to "$(pwd)"/data. Are you sure? [y/N]" response
case $response in
	[yY][eE][sS]|[yY])
		mkdir -p $(pwd)/data
		python `dirname $0`/create_iodata.py
		;;
	*)
		;;
esac
