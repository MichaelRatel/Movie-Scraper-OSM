# Python Web Scraper
Fork of jmoussa's IMDB Scraper that connects theater -> geopositional location. May no longer work due to IMDB's formatting update. 
Currently scrapes through imdb for nearby theaters and returns a json array of Theatre -> Movie & Showtimes + Location + OSM ID



### JSON Structure

```
[
    {
        "movies": [
            {
                "movie": "A Private War (2018)", 
                "times": [
                    "12:45 pm", 
                    "3:30", 
                    "6:15", 
                    "9:00"
                ]
            }, 
            {
                "movie": "A Star Is Born (2018)", 
                "times": [
                    "1:45 pm", 
                    "4:55"
                ]
            },
        ],
	"theatre": "Alamo Drafthouse Cinema - Downtown Brooklyn"
    "location": "445 Albee Square West, Brooklyn NY 11201"
    "mapID": "node/4620805945"
    }
]
```

### To Start

```
$ python scraping_imdb.py
```
Navigate to: localhost:5000/getMovies

Save the output as data.json, and place in the same directory
```
$ python format_csv.py
```
Will generate full output with dummy data