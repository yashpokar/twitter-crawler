from scrapy.loader import ItemLoader as DefaultItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

def strip(value):
	return value.replace('\n', '').replace('\t', '').strip()


class ItemLoader(DefaultItemLoader):
	default_input_processor = MapCompose(strip)
	default_output_processor = TakeFirst()


class TweetsLoader(ItemLoader):
	media_images_out = MapCompose(strip)
	media_videos_out = MapCompose(strip)

	text_out = Join()

	mentioned_user_id_out = MapCompose(strip)
	mentioned_user_url_out = MapCompose(strip)
