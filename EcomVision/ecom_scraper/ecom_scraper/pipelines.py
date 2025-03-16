# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os
import sys
import django
from asgiref.sync import sync_to_async

DJANGO_PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(DJANGO_PROJECT_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EcomVision.settings")
django.setup()

from user.models import *
from datetime import datetime

class MyScraperPipeline:
    def process_item(self, item, spider):
        return item


CATEGORY_MAPPING = {
    "smartphones": "mobile", "smartphone": "mobile", "phone": "mobile", "mobiles": "mobile", "iphone": "mobile", "basic mobiles": "mobile",
    "mobile chargers": "mobile accessories", "cases & covers": "mobile accessories", "mobile cables": "mobile accessories", "mobile holders": "mobile accessories", "mobile cases": "mobile accessories", "headphones & headsets": "mobile accessories", "power banks": "mobile accessories", "screenguards": "mobile accessories", "memory cards": "mobile accessories", "smart headphones": "mobile accessories", "cases & covers": "mobile accessories", "screen guards": "mobile accessories", "power banks": "mobile accessories", "headsets": "mobile accessories", "data cables": "mobile accessories", "chargers": "mobile accessories",
    "smart televisions": "televisions", "standard televisions": "televisions",
    "learning systems": "laptops",
}

class DjangoPipeline:
    async def process_item(self, item, spider):
        await sync_to_async(self.save_to_db)(item)
        return item
    
    def save_to_db(self, item):
        website, created = website_details.objects.get_or_create(
            base_url = item["w_url"],
            defaults={
                'website_name': item['w_name'],
            }
        )
        
        scraped_category = str(item["c_name"]).lower()
        print(f"Scraped_Category: {scraped_category}")
        standardized_category = CATEGORY_MAPPING.get(scraped_category, scraped_category)
        category, created = categories.objects.get_or_create(
            category_name = standardized_category
        )
        
        if created:
            print(f"category {category.category_name} added.")
            print(f"website {website.website_name} added.")
        else:
            print(f"category {category.category_name} already exists.")
            print(f"website {website.website_name} already exists.")
            
        price = item["p_price"]
        scraped_date = datetime.today().strftime('%Y-%m-%d')
        
        product, created = products.objects.update_or_create(
            product_id = item['p_id'],
            defaults={
                'website_id': website,
                'category_id': category,
                'product_name': item["p_name"],
                'product_price': {},
                'product_ratings': item["p_rating"],
                'product_details': item["p_details"],
                'currency': item["p_currency"],
                'is_available': item["p_available"],
                'product_url': item["p_url"],
                'product_image_url': item["p_images"],
            }
        )
        
        product_price_data = product.product_price
        
        if scraped_date in product_price_data:
            if product_price_data[scraped_date] == price:
                print(f"No price change for {product.product_name}. Skipping update.")
                return item
            print(f"Updating price for {product.product_name} on {scraped_date}")
            product_price_data[scraped_date] = price
        else:
            print(f"Appending new price entry for {product.product_name}.")
            product.product_price[scraped_date] = price
            
        product.product_price = product_price_data
        product.save()
        print(f"Updated price for {product.product_name}: {scraped_date} -> {price}")
            
        return item

class EcomScraperPipeline:
    def process_item(self, item, spider):
        return item
