class Movie:
  def __init__(self, title, url):
    self.title = title
    self.url = url

class Mirror:

    self.movies = []

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

