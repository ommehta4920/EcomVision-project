from django.db import models

# Create your models here.

class user_details(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_email = models.EmailField(max_length=100, unique=True)
    user_passwd = models.CharField(null=True, max_length=20)
    user_name = models.CharField(null=False, max_length=50)
    user_otp = models.CharField(null=True, max_length=10)

    def __str__(self):
        return f"{self.user_email} - {self.user_name}"


# Stores website details which are going to be scraped
class website_details(models.Model):
    website_id = models.AutoField(primary_key=True)
    website_name = models.CharField(null=False, max_length=100)
    base_url = models.URLField(null=False, unique=True)

    def __str__(self):
        return f"{self.website_name} - {self.base_url}"


# Stores product categories
class categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(null=False, unique=True, max_length=100)
    category_image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.category_id, self.category_name}"


# Stores product details
class products(models.Model):
    product_id = models.CharField(primary_key=True, max_length=550)
    product_name = models.CharField(null=False, max_length=500)
    product_price = models.JSONField(null=False)
    product_ratings = models.FloatField(null=False, default=dict)
    currency = models.CharField(null=False, max_length=10)
    product_details = models.JSONField(null=True)
    is_available = models.BooleanField(default=True)
    product_url = models.URLField(null=False, max_length=800)
    product_image_url = models.JSONField(null=True, default=dict)
    scraped_at = models.DateTimeField(auto_now_add=True)
    website_id = models.ForeignKey(website_details, on_delete=models.CASCADE)
    category_id = models.ForeignKey(categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product_name} - {self.product_price} - {self.product_url}"

    # Save The Product ID From the URL.


# Stores user's search requests
class user_request(models.Model):
    request_id = models.BigAutoField(primary_key=True)
    request_name = models.CharField(null=False, max_length=255)
    requested_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(user_details, on_delete=models.CASCADE)
    category_id = models.ForeignKey(categories, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.request_name}"


# Stores search requests' result
class request_result(models.Model):
    result_id = models.BigAutoField(primary_key=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    request_id = models.ForeignKey(user_request, on_delete=models.CASCADE)
    product_id = models.ForeignKey(products, on_delete=models.CASCADE)


# Stores the price tracking requests
class price_track(models.Model):
    status = [
        ('1', 'Active'),
        ('2', 'Completed'),
    ]
    track_id = models.BigAutoField(primary_key=True)
    desired_price = models.CharField(null=False, max_length=8)
    last_price = models.CharField(null=False, max_length=8)
    tracking_status = models.CharField(max_length=10, choices=status, default='1')
    user_id = models.ForeignKey(user_details, on_delete=models.CASCADE)
    product_id = models.ForeignKey(products, on_delete=models.CASCADE)
    category_id = models.ForeignKey(categories, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class contact_us(models.Model):
    contact_id = models.BigAutoField(primary_key=True)
    cont_name = models.CharField(null=False, max_length=50)
    cont_email = models.EmailField(null=False, max_length=40)
    message = models.TextField(null=False, max_length=700)

    def __str__(self):
        return f"{self.cont_name} - {self.cont_email} - {self.message}"

# class Socialaccount(models.Model):
#     socailaccount_id = models.BigAutoField(primary_key=True)
#     provider = models.CharField(null=False, max_length=200)
#     uid = models.CharField(null=False, max_length=200)
#     last_login = models.DateTimeField(auto_now_add=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     extra_data = models.JSONField(null=False)
#     user_id = models.ForeignKey(user_details, on_delete=models.CASCADE)
