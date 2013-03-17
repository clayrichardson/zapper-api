#! /bin/sh
# Script that compiles the less bundles in src to css
# files in this current directory.

GREEN="\033[1;32m"
RED="\033[1;31m"
RESET="\033[0m"

compile () {
	lessc src/$1.less $1.css
	echo $GREEN "compiled $1.css"
}

if ! type "lessc" > /dev/null 2>&1
then
	echo $RED "You must have the less compiler installed."
	echo $RED "To install it, you must first install the node package manager (npm)."
	echo $RED "Then install less via:"
	echo $GREEN "nmp install -g less"
elif [ -z "$1" ]
then
	echo $RED "You must supply the file name (without the extension) you wish to compile."
	echo $RED "You can compile all of the less bundles by running this script with the" $GREEN "all" $RED "argument"
elif [ "$1" = "all" ]
then
	for filename in src/*.less
	do
		NAME="$filename"
		NAME=${NAME:4}
		NAME=$(echo "$NAME" | sed 's/.\{5\}$//')
		compile $NAME
	done;
else
	if [ ! -f src/$1.less ]
	then
		echo $RED "src/$1.less does not exist. Nothing to compile."
	else
		compile $1
	fi
fi

printf $RESET
