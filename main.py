from prompt_toolkit import prompt
# from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.validation import Validator, ValidationError
from bs4 import BeautifulSoup
import urllib3
import re
import os

class Mirror:
    def __init__(self, name, search_path, urls):
        self.name = name
        self.search_path = search_path
        self.urls = urls

    def parse_search(self, search_dom):
        # TODO parse search dom
        pass

    def parse_movie(self, movie_dom):
        # TODO parse movie dom
        pass


# Order: name, search_path, urls
torrent_mirrors = [
    Mirror('1337x', '/search/%s/1/',
           [
               'https://1337x.wtf',
               'https://1337x.to'
           ]
           )
]

class ListIndexValidator(Validator):

    def __init__(self, reference):
        self.reference = reference

    def validate(self, document):
        text = str(document.text)

        if len(text) < 1:
            raise ValidationError(message="Input can't be empty")

        # Numeric checking code taken from https://python-prompt-toolkit.readthedocs.io/en/master/pages
        # /asking_for_input.html#asking-for-input
        if text and not text.isdigit():
            for _, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='Only numerics inputs are allowed.',
                                  cursor_position=len(text))

        list_length = len(self.reference)
        if int(text) >= list_length:
            raise ValidationError(
                message=f"Input out of range. Possible indexes: {'()' if list_length < 1 else '(0)' if list_length == 1 else f'(0-{list_length - 1})'}.",
                cursor_position=len(text))


def request_dom(url):
    http = urllib3.PoolManager()
    res = http.request("GET", url)

    return {'status': res.status, 'dom': res.data}

# Input

while True:
    print()
    print('Select a torrent mirror: ')

    for i in range(0, len(torrent_mirrors)):
        mirror = torrent_mirrors[i]
        print(f'{i} - ' + mirror.name)

    print()
    mirror_index = int(prompt('> ', validator=ListIndexValidator(torrent_mirrors), validate_while_typing=False))

    torrent_mirror = torrent_mirrors[mirror_index]

    print()
    movie_name = input('Movie: ')

    print()
    print(f'Searching on {torrent_mirror.name} for {movie_name}')

    attempts = len(torrent_mirrors)

    search_dom = None

    selected_url = None

    for i in range(0, attempts):
        selected_url = torrent_mirror.urls[i]

        url = selected_url + torrent_mirror.search_path % movie_name

        search_res = request_dom(url)

        if search_res['status'] == 404:
            print()
            print(f'An error occurred with the url: {url}. Trying another one...')
            continue
        elif search_res['status'] == 200:
            search_dom = str(search_res['dom'])
            break

    if search_dom is None:
        print()
        print(f'Impossible to get a working url from: {torrent_mirror.name}.')
        continue

    search_soup = BeautifulSoup(search_dom, 'html.parser')

    movie_table = search_soup.find('table')
    if movie_table is None:
        print()
        print('No movies were found...')
        continue

    movie_body = movie_table.find('tbody')
    found_movies = movie_body.find_all('a', href=re.compile('/torrent/'))

    if len(found_movies) < 1:
        print()
        print('No movies were found...')
        continue

    print()
    print('Select the movie:')
    print()
    # TODO create movie class to store all possible movie data
    available_movies = []
    for i in range(0, len(found_movies)):
        movie = found_movies[i]
        movie_name = movie.text
        movie_url = selected_url + movie.attrs['href']
        available_movies.append({'name': movie_name, 'url': movie_url})
        print(f'{i} - {movie_name}')

    print()
    movie_index = int(prompt('> ', validator=ListIndexValidator(available_movies), validate_while_typing=False))

    # TODO per mirror dom parsing
    movie = available_movies[movie_index]
    # Search for the magnet link

    movie_res = request_dom(movie['url'])

    movie_soup = BeautifulSoup(str(movie_res['dom']), 'html.parser')

    movie_magnet_tag = movie_soup.find('a', href=re.compile(r'magnet:'))

    movie_magnet_url = movie_magnet_tag.attrs['href']

    print()
    print("Trying to open on torrent desktop client.")
    os.system(f'webtorrent "{movie_magnet_url}" --vlc --player-args="--video-on-top --repeat"')