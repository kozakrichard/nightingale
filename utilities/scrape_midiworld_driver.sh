#! /bin/bash

# driver for the scrape_midiworld.py script to facilitate scraping all genres
# creates a directory for each genre and drops files in there

# files with spaces will have %20 instead, run below in each directory to fix:
# for f in *; do mv "$f" $(echo "$f" | sed 's/%20/-/g'); done

for genre in "pop" "classic" "rock" "rap" "dance" "punk" "blues" "country" "movie themes" "tv themes" "christmas carols" "video game themes" "disney themes" "national anthems" "jazz" "hip-hop";
do
	genre_dir=$(echo "$genre" | tr " " "-")
	mkdir "$genre_dir"
	cd "$genre_dir"
	python3 ../scrape_midiworld.py "$genre"
	cd ..
done
