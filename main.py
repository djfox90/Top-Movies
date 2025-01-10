from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import time


def top_movie():
    IMDB_URL = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm" #Top movie on imdb
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    }
    imdb_page = requests.get(IMDB_URL, headers=headers)

    imdb_top_movies = BeautifulSoup(imdb_page.content, "html.parser") #collect html data from website
    imdb_top_movies = BeautifulSoup(imdb_top_movies.prettify(), "html.parser")

    movie_titles = imdb_top_movies.find_all("h3") #Find movie titles
    movie_score = imdb_top_movies.find_all("span", class_="ipc-rating-star--rating")#Find movies scores
    movie_link = imdb_top_movies.find_all("a", class_="ipc-title-link-wrapper")#Find movies links to find movie generes

    movie_list_name = []
    movie_list_score = []
    keys = [
        "Action",
        "Drama",
        "Holiday",
        "Romance",
        "Fantasy",
        "Musical",
        "Horror",
        "Comedy",
        "Sci-Fi",
    ] # Create movie dict
    movie_dict = {key: False for key in keys} # makes all keys false
    action_list = []
    drama_list = []
    holiday_list = []
    romance_list = []
    fantasy_list = []
    musical_list = []
    horror_list = []
    comedy_list = []
    sci_fi_list = []

    for i in range(1, 11):# loop to collect top ten movies start at one to get rid of junk data

        movie_list_name.append(movie_titles[i].get_text().strip())
        movie_list_score.append(movie_score[i - 1].get_text().strip())
        link = movie_link[i - 1].get("href")
        link = "https://www.imdb.com/" + link

        MOVIE_URL = link # collect data from each movie link
        movie_page = requests.get(MOVIE_URL, headers=headers)
        imdb_movies = BeautifulSoup(movie_page.content, "html.parser")
        imdb_movies = BeautifulSoup(imdb_movies.prettify(), "html.parser")
        genres = imdb_movies.find_all("span", class_="ipc-chip__text")

        movie_dict = {key: False for key in keys}
        for i in range(len(genres) - 1):

            if genres[i].get_text().strip() in movie_dict:
                movie_dict[genres[i].get_text().strip()] = True

        action_list.append(movie_dict["Action"])
        drama_list.append(movie_dict["Drama"])
        holiday_list.append(movie_dict["Holiday"])
        romance_list.append(movie_dict["Romance"])
        fantasy_list.append(movie_dict["Fantasy"])
        musical_list.append(movie_dict["Musical"])
        horror_list.append(movie_dict["Horror"])
        comedy_list.append(movie_dict["Comedy"])
        sci_fi_list.append(movie_dict["Sci-Fi"])

    data = {
        "Titles": movie_list_name,
        "Score": movie_list_score,
        "Action": action_list,
        "Drama": drama_list,
        "Holiday": holiday_list,
        "Romance": romance_list,
        "Fantasy": fantasy_list,
        "Musical": musical_list,
        "Horror": horror_list,
        "Comedy": comedy_list,
        "Sci-Fi": sci_fi_list,
    }# data for dataframe
    df = pd.DataFrame(data)
    df["Rating"] = range(1, len(df) + 1) #rate each movie 1 to ten
    date = datetime.now()# get data to get month data was taken
    month = date.strftime("%B")
    df["Month"] = month# add the month for the top data
    

    if Path("/home/djfox232/Top-Movies/top_movies.csv").exists():
        df.to_csv("top_movies.csv", mode="a", index=False, header=False)# if file exist prevent repeat of column names
    else:
        df.to_csv("top_movies.csv", mode="a", index=False)


while True: # run program once a month
    top_movie()
    time.sleep(43200 * 60) 
