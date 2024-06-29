# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from PIL import Image
from io import BytesIO
import os




class BookscraperPipeline:
    def process_item(self, item, spider):
        return item

class CustomImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item["clean_image_urls"]:
            yield Request(image_url)

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return f'full/{image_guid}'

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                path = x['path']
                self.process_image(path)
        return item

    def process_image(self, path):
        image_path = os.path.join(self.store.basedir, path)
        image = Image.open(image_path)
        
        # Realiza algún procesamiento con Pillow, por ejemplo, redimensionar
        image = image.resize((128, 128))

        # Guarda la imagen procesada
        image.save(image_path)

    
