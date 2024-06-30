import scrapy
from bookscraper.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["www.foliosociety.com"]
    start_urls = ["https://www.foliosociety.com/row/fiction"]

    custom_settings = {
        "FEEDS" : {
        "bookdata.json" : {"format": "json" ,"overwrite": True},
        "bookscraper.csv" : {"format": "csv" ,"overwrite": True},
        }
    }

    def parse(self, response):
        books = response.css("ol li.item.product.product-item")
        for book in books:
            book_page = book.css("h3.product.name a").attrib["href"]
            yield response.follow(book_page, callback=self.parse_book_page)

        next_page = response.css("li.item.pages-item-next a.action.next").attrib["href"]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_book_page(self, response):
        book_item = BookItem()
        img_list = []
        book_item["url"] = response.url,
        book_item["title"] = response.css("div.columns h1.page-title span::text").get(),
        book_item["price"] =  response.css("div.box-tocart span.price::text").get(),
        book_item["author"] = response.css("div.columns p.book-attributes.book-attributes--author span::text").get(),
        book_item["illustrator"] = response.css("div.columns p.book-attributes.book-attributes--illustrator span::text").get(),
        book_item["introduceder"] = response.css("div.columns p.book-attributes.book-attributes--introduced span::text").get(),
        book_item["description"] = response.css("div.columns div.product-info-main div.value p").get(),
        #book_item["image"] = response.css("div.columns section.gallery-container ul li img::attr(src)").get(),
        for img in response.css("div.gallery-container__gallery ul.gallery li a img::attr(src)").getall():
            img_list.append(response.urljoin(img))
        book_item["clean_image_urls"] = img_list
        yield book_item



    
