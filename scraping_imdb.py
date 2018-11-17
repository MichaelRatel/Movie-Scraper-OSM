'''
Test of Beautiful Soup Scraping Library
    Scraping imdb.com for movies 
'''
from urllib2 import urlopen as uReq
from bs4 import BeautifulSoup as soup
import json
from flask import Flask, jsonify, request

MY_URL = 'https://www.imdb.com/showtimes/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=8872b8ce-ede1-42d7-ad7a-9ac8ef50b844&pf_rd_r=KZMHYANGCNHFXEFS589R&pf_rd_s=right-5&pf_rd_t=15061&pf_rd_i=homepage&ref_=hm_sh_lk1'
CLIENT = uReq(MY_URL)
PAGE_HTML = CLIENT.read()
CLIENT.close()

PAGE_SOUP = soup(PAGE_HTML, "html")
CONTAINERS = PAGE_SOUP.findAll('div', {"class":"list_item"})

theatreList = []

def addTheatre(dictionaryName, name, shows):
    dictionaryName['theatre'] = name
    dictionaryName['movies'] = shows
    theatreList.append(dictionaryName)

def get_all_info():
    #print "Theatres-----------"
    theatre_name = ''
    movie_title = ''
    showtimes = ''
    for container in CONTAINERS:
        theatre_name = container.div.a.getText()
        showsByTheatre = dict()
        if(len(theatre_name) > 2):
            #print 'Theatre: ' + theatre_name 
            movies = []
            for movie_container in container.findAll('div', {'class':'info'}):
                moviesAndShowtimes = dict()
                movie_title = movie_container.find('a', {'itemprop':'url'})
                #print '----------- Movies ' + movie_title.getText() 
                showtimes = map(lambda x:x.getText(), movie_container.findAll('a',{'rel':'nofollow'}))
                showtimeList = list(showtimes)
                moviesAndShowtimes['movie'] = movie_title.getText()
                moviesAndShowtimes['times'] = showtimeList
                movies.append(moviesAndShowtimes)
            addTheatre(showsByTheatre, theatre_name, movies)
    #print "-----------------"

app = Flask(__name__)

@app.route('/getMovies', methods=['GET'])
def get_movies():
    get_all_info()
    return json.dumps(theatreList, indent=4)
app.run(debug=True)
