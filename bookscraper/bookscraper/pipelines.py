# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html



# useful for handling different item types with a single interface
import re
from itemadapter import ItemAdapter
import mysql.connector


class BookscraperPipeline:

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        text = adapter.get("description")
        if isinstance(text, tuple):
            text = " ".join(text)
        clean_text = re.sub(r'<(\/?p|\/?em|\/?i|\/?span|\/?a)( [^>]*>|>)', '', text)
        adapter["description"] = clean_text

        field_names = adapter.field_names()
        for field_name in field_names:
            if (field_name != "price") and (field_name != "description"):
                value =  adapter.get(field_name)
                new_value = value[0]
                adapter[field_name] = new_value 
       
        money = adapter.get("price")
        money = " ".join(money)
        money = money.replace("£","")
        adapter["price"] = float(money)

        return item



class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = "127.0.0.1",
            user = "ivangalarza",
            password = "******",
            database = "books",
        )

        self.cur = self.conn.cursor()
        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS BooksData(
            id int NOT NULL auto_increment, 
            url TEXT,
            title TEXT,
            price DECIMAL,
            author TEXT,
            illustrator TEXT,
            introduceder TEXT,
            description TEXT,
            image TEXT,
            PRIMARY KEY (id)
        )
        """)

    def process_item(self, item, spider):

        self.cur.execute(""" insert into BooksData (
            url,
            title,
            price,
            author,
            illustrator,
            introduceder,
            description,
            image
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["price"],
            item["author"],
            item["illustrator"],
            item["introduceder"],
            item["description"],
            item["image"]
        ))

        self.conn.commit()

        return item

    def close_spider(self, spider):
 
        self.cur.close()
        self.conn.close()