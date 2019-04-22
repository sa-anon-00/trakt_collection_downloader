from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

HEADER = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'referrer': 'https://google.com'
    }

username = input('\nEnter your Trakt username: ')
url = "https://trakt.tv/users/" + username + "/collection/movies/added"

total_num = 0
films = {}
while True:
    response = requests.get(url, headers=HEADER, timeout=5)
    data = response.content
    soup = BeautifulSoup(data, "lxml")
    movies = soup.find_all("div", {"class": "grid-item"})

    for movie in movies:
        title = movie.find("meta", {"itemprop": "name"}).get("content")
        ratings = movie.find("div", {"class": "percentage"}).text
        date_added = datetime.strptime(movie.find("span", {"class": "format-date"}).text, "%Y-%m-%dT%H:%M:%SZ")
        poster = movie.find("img", {"class":"real"}).get("data-original")
        total_num += 1
        films[total_num] = [title, ratings, date_added, poster]
        print("\n"+3*"-----------------------------------------------")
        print("\ntitle:", title, "\nRatings:", ratings, "\nDate added:", date_added, "\nImage:", poster)

    next_page_url = soup.find("a", {"rel": "next"})
    try:
        if next_page_url.get("href"):
            url = "https://trakt.tv" + next_page_url.get("href")
            print(url)
        else:
            break

    except AttributeError:
        break


print("\nTotal number of movies: ", total_num)

films_df = pd.DataFrame.from_dict(films, orient= "index", columns= ["Title", "Ratings", "Dated added", "Poster"])
films_df.to_csv(f"{datetime.now():%Y_%m_%d}"+".csv")