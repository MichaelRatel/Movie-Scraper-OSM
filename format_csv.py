import json
import random
import csv
import math

# Format json file into CSV to read into PSQL
# json format is {theaterName, location, Movies[showtimes[]]}
# treat each theater -> movie -> showtime as its own key

def main():
    buildMovieTable()


def buildNormalTable():
    with open("data.json") as f:
        jsonData = json.load(f)
    with open("data.csv", "w") as fw:
        for item in jsonData:
            newlocation = item["location"].replace(",", "") #omit comma for csv
            for movie in item["movies"]:
                for showtime in movie["times"]:
                    if "am" not in showtime and "pm" not in showtime:
                        showtime = showtime + " pm"
                    fw.write(item["theatre"] + ", " + newlocation + ", " + item["mapID"] + ", " + movie["movie"] + ", " + showtime + "\n")
    pass

def buildUserTable():
    user = {}
    for id in range(1,1000):
        user[id] = {}
        user[id]["coordinates1"] = random.randrange(-90, 89) + random.random()
        user[id]["coordinates2"]= random.randrange(-90, 89) + random.random()
        
        user[id]["age"] = random.randint(18, 80)
        user[id]["radius"] = random.randint(25, 50)
        #print(user[id])
        pass
        
    with open("users.csv", "w") as fw:
        fw.write("ID,Age,Radius,Coordinates1,Coordinates2\n")
        for id in user.keys():
            fw.write(str(id) + "," + str(user[id]["age"]) + "," + str(user[id]["radius"]) + "," + str(user[id]["coordinates1"]) + "," + str(user[id]["coordinates2"]) + "\n")

def buildShowtimeTable():
    with open("data.json") as f:
        jsonData = json.load(f)
    with open("showtimes.csv", "w") as fw:
        moviecount = 0
        fw.write("Theater,Movie,Showtime,Screen,showID\n")
        for item in jsonData:
            newlocation = item["location"].replace(",", "") #omit comma for csv
            for movie in item["movies"]:
                for showtime in movie["times"]:
                    moviecount += 1
                    if "am" not in showtime and "pm" not in showtime:
                        showtime = showtime + " pm"
                    fw.write(item["theatre"] + "," + movie["movie"] + "," + showtime + ", " + str(random.randrange(0,10)) + "," + str(moviecount) + "\n")

def buildTheaterTable():
    with open("data.json") as f:
        jsonData = json.load(f)
    with open("export.geojson") as fr:
        baseTheaters = json.load(fr)
    features = baseTheaters["features"]
    with open("theaters.csv", "w") as fw:
        with open("theaterAmenities.csv", "w") as fw2:
            fw.write("Name,Phone,Email,ID,Coordinates,Screens\n")
            fw2.write("Name,isHearingAccessible,isWheelchairAccessible\n")
            for item in jsonData:
                newlocation = item["location"].replace(",", "") #omit comma for csv
                mapID = item["mapID"]
                # find coordinates
                coords = "idk"
                for node in features:
                    if node["properties"]["@id"] == mapID:
                        coordinates = node["geometry"]
                        if coordinates["type"] == "Polygon":
                            coords = str(coordinates["coordinates"][0][0]).replace(",", ":")
                            break
                        elif coordinates["type"] == "Point":
                            coords = str(coordinates["coordinates"]).replace(",", ":")
                            break
                        else:
                            coords = "unknown"
                            break
                    if coords == "idk":
                        coords = "unknown"
                # fabricate dummy extra data (phone number, email, screens)
                phone = "555" + str(random.randrange(1000000, 9999999)) #not going through effort to make unique, pray its unique, or just run again
                email = "dummyemail" + mapID[5:] + "@gmail.com"
                screencount = random.randrange(10, 20)
                fw.write(newlocation + "," + phone + "," + email + "," + mapID + "," + coords + "," + str(screencount) + "\n")
                fw2.write(newlocation + "," + str(random.randrange(0,2)) + "," + str(random.randrange(0,2)) + "\n")



    pass

def buildPricingTable():
    with open("showtimes.csv", "r") as f:
        csvFile = csv.DictReader(f)
        savedPrices = {}
        with open("pricings.csv", "w") as fw:
            with open("bookings.csv", "w") as fw2:
                for item in csvFile:
                    adult = random.randrange(10, 15)
                    senior = random.randrange(5,12)
                    savedPrices[item["showID"]] = adult
                    fw.write(item["showID"] + ",Adult," + str(adult) + "\n")
                    fw.write(item["showID"] + ",Senior," + str(senior) + "\n")

                    fw2.write(item["showID"] + "," + str(random.randrange(0,200)) + "," + str(adult) + "\n")               

def buildTravelPaths():
    with open("users.csv", "r") as f:
        csvFile = csv.DictReader(f)
        with open("theaters.csv", "r") as fr:
            theaterFile = csv.DictReader(fr)
            with open("paths.csv", "w") as fw:
                fw.write("userLoc,theaterLoc,TravelPath,Distance,Time\n")
                for item in csvFile:
                    coords1 = item["Coordinates1"]
                    coords2 = item["Coordinates2"]
                    coords = "[" + coords1 + ": " + coords2 + "]"
                    
                    for theater in theaterFile:
                        theaterCoords = theater["Coordinates"]
                        path = coords + " going to " + theaterCoords
                        distance = float(random.randrange(1000, 200000))
                        time = distance / 8000
                        fw.write(coords + "," + theaterCoords + "," + path + "," + str(distance) + "," + str(time) + "\n")
                        
def buildMovieTable():
    with open("showtimes.csv", "r") as f:
        with open("movies.csv", "w") as fw:
            csvFile = csv.DictReader(f)
            movieList = []
            for item in csvFile:
                if item["Movie"] in movieList:
                    pass
                else:
                    # These all needed to be fabricated due to IMDB banning my scraper.
                    title = item["Movie"]
                    movieList.append(item["Movie"])
                    rtRating = str(random.randrange(0,100))
                    age = random.random()
                    if age < .2:
                        rating = "G"
                    elif age < .4:
                        rating = "PG"
                    elif age < .6:
                        rating = "PG-13"
                    else:
                        rating = "R"
                    link = item["Movie"] + "'s IMDB link"
                    imdbID = item["Movie"] + "'s IMDB ID"
                    fw.write(title + "," + str(random.randrange(60, 180)) + "," + rtRating + "," + rating + "," + link + "," + imdbID + "\n")

                
def buildCastTable():
    with open("showtimes.csv", "r") as f:
        with open("cast.csv", "w") as fw:
            csvFile = csv.DictReader(f)
            movieList = []
            for item in csvFile:
                if item["Movie"] in movieList:
                    pass
                else:
                    movieList.append(item["Movie"])
            fw.write("Cast,Role,Movie\n")
            for i in range (0,500):
                for j in range (0, 5):
                    curMovie = movieList[math.floor(random.random() * len(movieList))]
                    line = "Dummy Cast " + str(i) + ",Actor," + curMovie + "\n"
                    fw.write(line)

def buildPersonTypeTable(): 
    pass # DO THIS MANUALLY IN POSTGRES


if __name__ == "__main__":
    main()