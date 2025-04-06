from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(categories)
admin.site.register(products)
admin.site.register(website_details)
admin.site.register(user_details)
