'''
Test of Beautiful Soup Scraping Library
    Scraping imdb.com for movies 
'''
import time
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup
import json
from flask import Flask, jsonify, request
import overpy


MY_URL = 'https://www.imdb.com/showtimes/US/'
CLIENT = uReq('https://www.imdb.com/showtimes/US/14726')
PAGE_HTML = CLIENT.read()
CLIENT.close()

PAGE_SOUP = BeautifulSoup(PAGE_HTML, "lxml")
CONTAINERS = PAGE_SOUP.findAll('div', {"class":"list_item"})
OSM = overpy.Overpass()

NY_ZIP_CODES = range(10000, 14672) # use for collecting entire set
BROOKLYN_ZIP_CODES = range(10000, 10100) # use for testing overlapping datapoints
UB_ZIP_CODES = range(14261, 14262) # use for testing small subsets quickly

theatreList = []
foundTheatres = []

def addTheatre(dictionaryName, name, shows, location):
    foundTheatres.append(name)
    dictionaryName['theatre'] = name
    dictionaryName['location'] = location
    dictionaryName['movies'] = shows
    theatreList.append(dictionaryName)

def get_all_info():
    #print "Theatres-----------"
    theatre_name = ''
    movie_title = ''
    showtimes = ''
    theatre_address = ''

    startTime = time.time()
    for zip in range(14261, 14262): 
        currentClient = uReq(MY_URL + str(zip))
        curHTML = currentClient.read()
        currentClient.close()
        page = BeautifulSoup(curHTML, "html")
        CONTAINERS = PAGE_SOUP.findAll('div', {"itemtype":"http://schema.org/MovieTheater"})
        for container in CONTAINERS:
            theatre_name = container.div.a.getText()
            if theatre_name in foundTheatres:
                continue
            theatre_address = container.find('div', {'class' : 'address'}).find('div').getText().split('|')[0].strip().replace("\n", " ")
            
            showsByTheatre = dict()
            if(len(theatre_name) > 2 and not (theatre_name in foundTheatres) ):
                print ("Theatre: " + theatre_name )
                movies = []
                for movie_container in container.findAll('div', {'class':'info'}):
                    moviesAndShowtimes = dict()
                    movie_title = movie_container.find('a', {'itemprop':'url'})

                    showtimes = map(lambda x:x.getText().strip(), movie_container.findAll('a',{'rel':'nofollow'}))
                    showtimeList = list(showtimes)

                    moviesAndShowtimes['movie'] = movie_title.getText()
                    moviesAndShowtimes['times'] = showtimeList
                    movies.append(moviesAndShowtimes)
                addTheatre(showsByTheatre, theatre_name, movies, theatre_address)
        #print "-----------------"
    endtime = time.time()
    elapsed = endtime - startTime
    print("Elapsed time for query: " + elapsed)

app = Flask(__name__)

@app.route('/getMovies', methods=['GET'])
def get_movies():
    get_all_info()
    return json.dumps(theatreList, indent=4)
app.run(debug=True)
