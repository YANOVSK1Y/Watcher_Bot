import requests

def search_by_keywords(title_name):
    url = "https://data-imdb1.p.rapidapi.com/movie/byKeywords/{}/".format(title_name)
    headers = {
        'x-rapidapi-host': "data-imdb1.p.rapidapi.com",
        'x-rapidapi-key': "326464ff3amsh674dfa024b73900p1ea129jsn8e9dc57a23a1"
        }
    response = requests.request("GET", url, headers=headers)
    return response.json()


def search_by_titlename(title_name):
    url = "https://data-imdb1.p.rapidapi.com/movie/imdb_id/byTitle/{}/".format(title_name)
    headers = {
        'x-rapidapi-host': "data-imdb1.p.rapidapi.com",
        'x-rapidapi-key': "326464ff3amsh674dfa024b73900p1ea129jsn8e9dc57a23a1"
        }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def search_by_imdb_id(imdb_id):
    url = f"https://data-imdb1.p.rapidapi.com/movie/id/{imdb_id}/"
    headers = {
        'x-rapidapi-host': "data-imdb1.p.rapidapi.com",
        'x-rapidapi-key': "326464ff3amsh674dfa024b73900p1ea129jsn8e9dc57a23a1"
        }
    response = requests.request("GET", url, headers=headers)
    return response.json()

def search_by_rating():
    url = "https://data-imdb1.p.rapidapi.com/movie/order/byRating/"
    headers = {
        'x-rapidapi-host': "data-imdb1.p.rapidapi.com",
        'x-rapidapi-key': "326464ff3amsh674dfa024b73900p1ea129jsn8e9dc57a23a1"
        }
    response = requests.request("GET", url, headers=headers)
    return response.json()
