from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import time

def top_movie():
    IMDB_URL = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    }
    imdb_page = requests.get(IMDB_URL, headers=headers)
    
    
    
    imdb_top_movies = BeautifulSoup(imdb_page.content, "html.parser")
    imdb_top_movies = BeautifulSoup(imdb_top_movies.prettify(), "html.parser")
    
    movie_titles = imdb_top_movies.find_all("h3")
    movie_score = imdb_top_movies.find_all("span", class_="ipc-rating-star--rating")
    movie_link = imdb_top_movies.find_all("a", class_="ipc-title-link-wrapper")
   
    movie_list_name=[]
    movie_list_score=[]
    keys =["Action" , "Drama", "Holiday", "Romance", "Fantasy", "Musical","Horror"]
    movie_dict =  {key: False for key in keys}
    action_list =[]
    drama_list = []
    holiday_list = []
    romance_list = []
    fantasy_list = []
    musical_list = []
    horror_list = []
       
    for i in range(1,11):
        
        movie_list_name.append(movie_titles[i].get_text().strip())
        movie_list_score.append(movie_score[i-1].get_text().strip())
        link=movie_link[i-1].get('href')
        link="https://www.imdb.com/"+link
        
       
        MOVIE_URL = link
        movie_page = requests.get(MOVIE_URL, headers=headers)
        imdb_movies = BeautifulSoup(movie_page.content, "html.parser")
        imdb_movies = BeautifulSoup(imdb_movies.prettify(), "html.parser")
        genres = imdb_movies.find_all("span", class_="ipc-chip__text")
        
        movie_dict =  {key: False for key in keys}
        for i in range(len(genres)-1):
            
            if genres[i].get_text().strip() in movie_dict:
                movie_dict[genres[i].get_text().strip()] = True
        
        
        action_list.append(movie_dict["Action"]) 
        drama_list.append(movie_dict["Drama"])
        holiday_list.append(movie_dict["Holiday"])
        romance_list.append(movie_dict["Romance"])
        fantasy_list.append(movie_dict["Fantasy"])
        musical_list.append(movie_dict["Musical"])
        horror_list.append(movie_dict["Horror"])
   
    
    data = {"Titles": movie_list_name, "Score": movie_list_score, "Action": action_list, "Drama": drama_list,"Holiday": holiday_list, "Romance":romance_list, "Fantasy":fantasy_list, "Musical":musical_list,"Horror":horror_list}
    df = pd.DataFrame(data)
    df['Rating'] = range(1, len(df) + 1)
    date = datetime.now()
    month = date.strftime("%B")
    df['Month'] = month
    print(df)
    
    if Path("/home/djfox232/Top-Movies/test_4.csv").exists():
        df.to_csv("test_4.csv",mode="a",index=False, header=False)
    else:
        df.to_csv("test_4.csv",mode="a",index=False)
    
    
while True:
    top_movie() 
    time.sleep(43200*60)
    
    
    
    