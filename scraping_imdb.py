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
import jellyfish

MY_URL = 'https://www.imdb.com/showtimes/US/'
CLIENT = uReq('https://www.imdb.com/showtimes/US/14726')
PAGE_HTML = CLIENT.read()
CLIENT.close()

PAGE_SOUP = BeautifulSoup(PAGE_HTML, "html")
CONTAINERS = PAGE_SOUP.findAll('div', {"class":"list_item"})
OSM = overpy.Overpass()

NY_ZIP_CODES = range(10000, 14672, 15) # use for collecting entire set
BROOKLYN_ZIP_CODES = range(10000, 10100, 15) # use for testing overlapping datapoints
UB_ZIP_CODES = range(14261, 14262, 15) # use for testing small subsets quickly

# load OSM data of all movie theaters in NY
with open("export.geojson") as f:
    baseTheaters = json.load(f)
features = baseTheaters["features"]
addrToID = {}

def buildAddrToID():
    for cinema in features:
        x = cinema["properties"]
        #print(x.keys())
        if "addr:street" not in x.keys() or "addr:housenumber" not in x.keys() or "addr:city" not in x.keys() or "addr:postcode" not in x.keys():
            continue
        addr = x["addr:housenumber"] + " " + x["addr:street"] + ", " + x["addr:city"].lstrip() + " " + "NY" + " " + x["addr:postcode"]
        addrToID[addr] = x["@id"]
        pass
    pass


theatreList = []
foundTheatres = []

# Add theatre to dictionary, compiling its name, showtimes, location, and OSM ID
def addTheatre(dictionaryName, name, shows, location):
    foundTheatres.append(name)
    dictionaryName['theatre'] = name
    dictionaryName['location'] = location
    min_distance = 50
    best_match = ""
    for loc in addrToID.keys():
        s = jellyfish.levenshtein_distance(loc, location)
        if s < min_distance:
            min_distance = s
            best_match = loc
    dictionaryName['mapID'] = addrToID[best_match]
    dictionaryName['movies'] = shows
    theatreList.append(dictionaryName)

def get_all_info():
    #print "Theatres-----------"
    theatre_name = ''
    movie_title = ''
    showtimes = ''
    theatre_address = ''
    buildAddrToID()
    #print(addrToID["4276 Maple Road, Amherst NY 14226"])
    startTime = time.time()
    for zip in NY_ZIP_CODES: 
        currentClient = uReq(MY_URL + str(zip))
        curHTML = currentClient.read()
        currentClient.close()
        PAGE_SOUP = BeautifulSoup(curHTML, "html")
        CONTAINERS = PAGE_SOUP.find_all('div', {"itemtype":"http://schema.org/MovieTheater"})
        for container in CONTAINERS:
            theatre_name = container.div.a.getText()
            if theatre_name in foundTheatres:
                continue
            theatre_address = container.find('div', {'class' : 'address'}).find('div').getText().split('|')[0].replace("\n", " ").replace(",         ", ", ").strip()
            showsByTheatre = dict()
            if(len(theatre_name) > 2 and not (theatre_name in foundTheatres) ):
                print ("Theatre: " + theatre_name )
                movies = []
                for movie_container in container.find_all('div', {'class':'info'}):
                    moviesAndShowtimes = dict()
                    movie_title = movie_container.find('a', {'itemprop':'url'})

                    showtimes = map(lambda x:x.getText().strip(), movie_container.find_all('a',{'rel':'nofollow'}))
                    showtimeList = list(showtimes)
                    if movie_title is None:
                        continue
                    moviesAndShowtimes['movie'] = movie_title.getText()
                    moviesAndShowtimes['times'] = showtimeList
                    movies.append(moviesAndShowtimes)
                addTheatre(showsByTheatre, theatre_name, movies, theatre_address)
        #print "-----------------"
    endtime = time.time()
    elapsed = endtime - startTime
    #print(addrToID)
    print(elapsed)

app = Flask(__name__)

@app.route('/getMovies', methods=['GET'])
def get_movies():
    
    get_all_info()
    with open("data.json", "w") as f:
        json.dump(theatreList, f)
    return json.dumps(theatreList, indent=4)
app.run(debug=True)
