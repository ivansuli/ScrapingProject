# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from PIL import Image
import os
import re




class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        descrip = adapter.get("description")
        text = descrip[0]
        clean_text = re.sub(r'<(\/?p|\/?em|\/?i|\/?span|\/?a)( [^>]*>|>)', '', text)
        adapter["description"] = clean_text
        return item

class CustomImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """adapter = ItemAdapter(item)
        image = adapter["image"]
        item["clean_image_urls"].append(image[0])"""
        for image_url in item["clean_image_urls"]:
            print(f'Requesting image: {image_url}')  # Imprime las URLs de las imágenes solicitadas
            yield Request(image_url)

    def file_path(self, request, response=None, info=None):
        image_split = request.url.split('/')[-1]
        image_guid = image_split.split("?")[0] 
        path = f'full/{image_guid}'
        print(f'Saving image to: {path}')  # Imprime la ruta de guardado
        return path

    def item_completed(self, results, item, info):
        for ok, x in results:
            if ok:
                path = x['path']
                self.process_image(path)
        return item

    def process_image(self, path):
        image_path = os.path.join(self.store.basedir, path)
        print(f'Processing image: {image_path}')  # Imprime la ruta de la imagen a procesar
        with Image.open(image_path) as image:
            image = image.resize((700, 700))
            image.save(image_path)

    
