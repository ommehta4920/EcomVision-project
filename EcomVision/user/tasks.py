from celery import shared_task
import subprocess
import os

from EcomVision import settings
from .models import categories, price_track
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True)
def categoryScrapper(self):
    # print("This is Category Scrapper.")
    categoryNames = categories.objects.values_list('category_name', flat=True)
    project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ecom_scraper")
    if not categoryNames:
        print("No Categories found in the database!")
    else:
        for categoryName in categoryNames:
            print(f"Scrapping data for Category: {categoryName}")
            subprocess.run(["scrapy", "crawl", "ecom_spider", "-a", f"query={categoryName}"], cwd=project_path)
    return "Category-Scrapping Done"

@shared_task(bind=True)
def productScrapper(self):
    # print("This is product Scrapper")
    project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ecom_scraper")
    subprocess.run(["scrapy", "crawl", "productSpider"], cwd=project_path)
    return "Product-Scrapping Done"

@shared_task(bind=True)
def check_price_tracking():
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)
    
    tracks = price_track.objects.filter(tracking_status='1')
    
    for track in tracks:
        try:
            current_price = float(track.last_price)
            desired_price = float(track.desired_price)
            
            if current_price <= desired_price:
                send_mail(
                    subject='🎉 Price Drop Alert From EcomVision!',
                    message=f'The product "{track.product_id.product_name}" is now ₹{current_price}, which is at or below your desired price of ₹{desired_price}.',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[track.user_id.user_email],
                    fail_silently=False,
                )
                track.tracking_status = '2'
                track.save()
                continue
            
            if hasattr(track, 'created_at') and track.created_at < one_week_ago:
                track.tracking_status = '2'
                track.save()
        except Exception as e:
            print(f"Error Processing track {track.track_id}: {e}")