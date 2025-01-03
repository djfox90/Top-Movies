from bs4 import BeautifulSoup
import requests

def top_movie():
    IMDB_URL = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    }
    imdb_page = requests.get(IMDB_URL, headers=headers)
    
    print(IMDB_URL)
    print(imdb_page)
    
    imdb_top_movies = BeautifulSoup(imdb_page.content, "html.parser")
    imdb_top_movies = BeautifulSoup(imdb_top_movies.prettify(), "html.parser")
    movie_titles = imdb_top_movies.find_all("h3")
    print(movie_titles[1].get_text())
    
top_movie()
    