import json




# Format json file into CSV to read into PSQL
# json format is {theaterName, location, Movies[showtimes[]]}
# treat each theater -> movie -> showtime as its own key

def main():
    buildShowtimeTable()


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

def buildShowtimeTable():
    with open("data.json") as f:
        jsonData = json.load(f)
    with open("data.csv", "w") as fw:
        for item in jsonData:
            newlocation = item["location"].replace(",", "") #omit comma for csv
            for movie in item["movies"]:
                for showtime in movie["times"]:
                    if "am" not in showtime and "pm" not in showtime:
                        showtime = showtime + " pm"
                    fw.write(item["theatre"] + "," + movie["movie"] + "," + showtime + "\n")


if __name__ == "__main__":
    main()