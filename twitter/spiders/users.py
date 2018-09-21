import json
from ..items import Profile, Tweet
from ..loaders import ItemLoader, TweetsLoader
from scrapy.selector import Selector
import scrapy


class UsersSpider(scrapy.Spider):
	name = 'users'

	custom_settings = {
		'JOBDIR': 'crawls/users-1',
	}

	start_urls = [
		'https://twitter.com/@katyperry',
		'https://twitter.com/@narendramodi',
		'https://twitter.com/@virendersehwag',
		'https://twitter.com/@KapilSharmaK9',
	]

	def parse(self, response):
		max_position = response.xpath('//div[@data-max-position]/@data-max-position').extract_first()

		if max_position:
			yield scrapy.Request('https://twitter.com/i/profiles/show/justinbieber/timeline/tweets?include_available_features=1&include_entities=1&max_position={}&reset_error_state=false'.format(max_position), callback=self.paginate_tweets)

		il = ItemLoader(Profile(), response)

		il.add_xpath('cover_image', '//*[@class="ProfileCanopy-headerBg"]/img/@src')
		il.add_xpath('image', '//*[contains(@class, "ProfileAvatar-image")]/@src')
		il.add_xpath('name', '//a[contains(@class, "ProfileNameTruncated-link")]/text()')
		il.add_xpath('username', '//div[@class="ProfileCardMini-screenname"]//b/text()')
		il.add_xpath('id', '//div[@class="ProfileNav"][@data-user-id]/@data-user-id')
		il.add_xpath('tweets', '//li[contains(@class, "ProfileNav-item--tweets")]//span[@class="ProfileNav-value"]/@data-count')
		il.add_xpath('following', '//li[contains(@class, "ProfileNav-item--following")]//span[@class="ProfileNav-value"]/@data-count')
		il.add_xpath('followers', '//li[contains(@class, "ProfileNav-item--followers")]//span[@class="ProfileNav-value"]/@data-count')
		il.add_xpath('favorites', '//li[contains(@class, "ProfileNav-item--favorites")]//span[@class="ProfileNav-value"]/@data-count')
		il.add_xpath('location', '//div[contains(@class, "ProfileHeaderCard-location")]//a/text()')
		il.add_xpath('location_page', '//div[contains(@class, "ProfileHeaderCard-location")]//a/@href')
		il.add_xpath('location_id', '//div[contains(@class, "ProfileHeaderCard-location")]//a/@data-place-id')
		il.add_xpath('website', '//div[contains(@class, "ProfileHeaderCard-urlText")]/a/@href')
		il.add_xpath('join_date', '//div[@class="ProfileHeaderCard-joinDate"]//span[@title]/@title')
		il.add_xpath('birthdate', '//span[contains(@class, "ProfileHeaderCard-birthdateText")]//text()')
		il.add_xpath('bio', '//p[contains(@class, "ProfileHeaderCard-bio")]//text()')
		il.add_xpath('media', '//a[contains(@class, "PhotoRail-headingWithCount")]/text()')
		il.add_xpath('media_url', '//a[contains(@class, "PhotoRail-headingWithCount")]/@href')
		il.add_value('table', 'users')

		yield il.load_item()

		for tweet in response.xpath('//ol[@id="stream-items-id"]/li'):
			for user in list(set(tweet.xpath('.//a[@data-mentioned-user-id]/@href').extract())):
				self.logger.info(f'Scheduling {user}\' account now')
				yield scrapy.Request(f'https://twitter.com{user}')

			yield self.parse_tweets(tweet)

	def parse_tweets(self, selector):
		tl = TweetsLoader(Tweet(), selector=selector)

		tl.add_xpath('id', './/li[@data-item-id]/@data-item-id')
		tl.add_xpath('user_id', './/div[@data-user-id]/@data-user-id')
		tl.add_xpath('on', './/small[@class="time"]/a/@title')
		tl.add_xpath('url', './/small[@class="time"]/a/@href')
		tl.add_xpath('conversation_id', './/small[@class="time"]/a/@data-conversation-id')
		tl.add_xpath('text', './/p[contains(@class, "TweetTextSize")]//text()')
		tl.add_xpath('replies', './/span[contains(@class, "ProfileTweet-action--reply")]//span[@class="ProfileTweet-actionCount"]/@data-tweet-stat-count')
		tl.add_xpath('retweets', './/span[contains(@class, "ProfileTweet-action--retweet")]//span[@class="ProfileTweet-actionCount"]/@data-tweet-stat-count')
		tl.add_xpath('favorites', './/span[contains(@class, "ProfileTweet-action--favorite")]//span[@class="ProfileTweet-actionCount"]/@data-tweet-stat-count')
		tl.add_xpath('mentioned_user_id', './/a[@data-mentioned-user-id]/@data-mentioned-user-id')
		tl.add_xpath('mentioned_user_url', './/a[@data-mentioned-user-id]/@href')

		tl.add_xpath('media_images', './/div[contains(@class, "AdaptiveMedia-photoContainer")]/@data-image-url')
		tl.add_xpath('media_videos', './/video/@src')
		tl.add_value('table', 'tweets')

		return tl.load_item()

	def paginate_tweets(self, response):
		response = json.loads(response.body)

		if response['has_more_items']:
			yield scrapy.Request('https://twitter.com/i/profiles/show/justinbieber/timeline/tweets?include_available_features=1&include_entities=1&max_position={}&reset_error_state=false'.format(response['min_position']), callback=self.paginate_tweets)

		selector = response['items_html']
		yield self.parse_tweets(Selector(text=selector))
