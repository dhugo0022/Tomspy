from bs4 import BeautifulSoup

# Media Option Types
__media_options = [
  "Movies",
  "Tv",
  "Anime",
]

# Media Source List
__source_list = {
  "1337x": {
    "general_search_url": "https://www.1377x.to/search/{title}/1/",
    "caterogy_search_url": "https://www.1377x.to/category-search/{title}/{category}/1/",
    "find_number_of_pages": lambda soup:
      soup.find("div", {"class": "pagination"})
      

    "find_media_list_in_page": lambda html: #TODO find media list in page
  },
  "LimeTorrents": {
    "general_search_url": "https://www.limetorrents.lol/search/all/{title}/1",
    "caterogy_search_url": "https://www.limetorrents.lol/search/{category}/{title}/1/",
    "find_number_of_pages": lambda html: #TODO find page
    "find_media_list_in_page": lambda html: #TODO find media list in page
  }
}

def search_media(title, source, deep_search = False):
  source_object = __source_list[source]
  url = source_object.base_url


  return {
    "title": title,
    "source": source,
  }