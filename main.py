from bs4 import BeautifulSoup
import requests

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
    movie_list_link=[]
    for i in range(1,21):
        
        movie_list_name.append(movie_titles[i].get_text().strip())
        movie_list_score.append(movie_score[i-1].get_text().strip())
        link=movie_link[i].get('href')
        link="https://www.imdb.com/"+link
        movie_list_link.append(link)
        
       
   
    
    
        
    
def movie_genere():
    MOVIE_URL = "https://www.imdb.com//title/tt1262426/?ref_=chtmvm_t_2"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
    }
    movie_page = requests.get(MOVIE_URL, headers=headers)
    imdb_movies = BeautifulSoup(movie_page.content, "html.parser")
    imdb_movies = BeautifulSoup(imdb_movies.prettify(), "html.parser")
    
    genres = imdb_movies.find_all("span", class_="ipc-chip__text")
    print(genres[1].get_text())
movie_genere()
    
    
    
    