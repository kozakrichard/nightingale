#https://freemidi.org/genre
"""
todo
- handle pagination (artist page has multiple pages)
	+ https://freemidi.org/artist-284-blink-182-P-3
	+ just add the -P-1, -P-2, -P-3 until it sends a 404
- figure out how to get actual file from download page
	+ ajax post request nonsense
	+ selenium simulate click?
"""

import requests
import urllib
from bs4 import BeautifulSoup
import sys

USER_AGENT = 'curl/7.54.0' # why not lmfao
HEADERS = {'user-agent': USER_AGENT}

CATEGORIES = [
	"rock",
	"pop",
	"hip-hop-rap",
	"rnb-soul",
	"classical",
	"country",
	"jazz",
	"blues",
	"dance-eletric",
	"folk",
	"punk",
	"newage",
	"reggae-ska",
	"metal",
	"disco",
	"bluegrass"
]

#for unique file names, e.g. "1-1.midi", "2-5.midi"
n_artist = 1
n_song = 1

def error(*msg, displayGenres=False):
	print(*msg)
	if(displayGenres):
		print("Available genres:\n *", "\n * ".join(CATEGORIES))
	exit(1)

def scrapeSong(song_page):
	url = "https://freemidi.org/" + song_page
	response = requests.get(url, headers=HEADERS)
	if response.status_code != 200:
		return

	html = response.text
	soup = BeautifulSoup(html, 'html.parser')
	href = soup.find("a", {"id": "downloadmidi"}).get("href")
	url = "https://freemidi.org/" + href

	fn = str(n_artist) + "-" + str(n_song) + ".midi"
	try: urllib.request.urlretrieve(url, fn)
	except urllib.error.HTTPError:
		return
	print("* Downloading", fn, end="\r")

def scrapeArtist(artist_page):
	global n_song
	global n_artist

	url = "https://freemidi.org/" + artist_page
	response = requests.get(url, headers=HEADERS)
	if response.status_code != 200:
		return
	html = response.text
	soup = BeautifulSoup(html, 'html.parser')

	#first two results are not songs
	for song in soup.find_all("a", itemprop="url")[2:]:
		scrapeSong(song.get("href"))
		n_song += 1

	n_artist += 1
	n_song = 1
	print()

def scrape(genre):
	genre = urllib.parse.quote(genre)

	url = "https://freemidi.org/genre-" + genre 
	response = requests.get(url, headers=HEADERS)
	if response.status_code != 200:
		return

	html = response.text
	soup = BeautifulSoup(html, 'html.parser')

	for artist in soup.find_all("div", class_="genre-link-text"):
		scrapeArtist(artist.a.get("href"))

def main():
	if len(sys.argv) != 2:
		error("Usage:", sys.argv[0], "<genre>", displayGenres=True)
	else:
		if sys.argv[1] not in CATEGORIES:
			error("No such genre.", displayGenres=True)
		else:
			scrape(sys.argv[1])
try:
	main()
except KeyboardInterrupt:
	exit(0)
