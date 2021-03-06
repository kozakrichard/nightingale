#!/bin/bash

if [ $# -ne 1 ] || [ "$1" = "-h" ] || [ "$1" == "--help" ]; then
	echo "Usage: $(basename $0) <directory to clean>"
	echo "Removes all non-midi files from specified directory"
	exit
elif [ ! -d "$1" ]; then
	echo "$1 is not a valid directory"
	exit
fi

for f in "$1"/*; do
	ret=$(file "$f" | grep "MIDI")
	if [ -z "$ret" ]; then
		echo "$f is not a midi file..."
		file "$f"
		echo "---"
		rm "$f"
	fi
done
