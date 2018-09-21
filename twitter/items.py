import scrapy


class Item(scrapy.Item):
	table = scrapy.Field()


class Profile(Item):
	cover_image = scrapy.Field()
	image = scrapy.Field()
	name = scrapy.Field()
	username = scrapy.Field()
	id = scrapy.Field()
	tweets = scrapy.Field()
	following = scrapy.Field()
	followers = scrapy.Field()
	favorites = scrapy.Field()
	location = scrapy.Field()
	location_page = scrapy.Field()
	location_id = scrapy.Field()
	website = scrapy.Field()
	join_date = scrapy.Field()
	birthdate = scrapy.Field()
	bio = scrapy.Field()
	media = scrapy.Field()
	media_url = scrapy.Field()


class Tweet(Item):
	id = scrapy.Field()
	user_id = scrapy.Field()
	on = scrapy.Field()
	url = scrapy.Field()
	conversation_id = scrapy.Field()
	text = scrapy.Field()
	replies = scrapy.Field()
	retweets = scrapy.Field()
	favorites = scrapy.Field()
	mentioned_user_id = scrapy.Field()
	mentioned_user_url = scrapy.Field()
	media_images = scrapy.Field()
	media_videos = scrapy.Field()
