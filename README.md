# Python Web Scraper 
Currently scrapes through imdb for nearby theaters and returns a json array of Theatre -> Movie & Showtimes



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
		"theatre": "AMC Loews New Brunswick 18"
	}
]
```

### To Start

```
$ python scraping_imdb.py
```
Navigate to: localhost:5000/getMovies
