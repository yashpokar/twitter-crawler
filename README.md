# twitter-crawler
Twitter scrapy project

> seriously twitter has no throttling strategy. Don't know why. May be at least someone is accessing twitter. 

change your mongodb setting,

put `MONGO_URI = 'your mongo uri'` and `MONGO_DATABASE = 'your database name'` 
in settings.py

then in your terminal following command,
``
scrapy crawl users
``
