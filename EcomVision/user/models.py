from django.db import models

# Create your models here.

class user_details(models.Model):
    user_email = models.EmailField(primary_key=True, max_length=100)
    user_passwd = models.CharField(null=False, max_length=20)
    user_name = models.CharField(null=False, max_length=50)
    user_otp = models.CharField(null=True, max_length=10)

    # def __str__(self):
    #     return f"{self.user_email} - {self.user_name}"


# Stores website details which are going to be scraped
class website_details(models.Model):
    website_id = models.AutoField(primary_key=True)
    website_name = models.CharField(null=False, max_length=100)
    base_url = models.URLField(null=False, unique=True, max_length=100)

    def __str__(self):
        return f"{self.website_name} - {self.base_url}"


# Stores product categories
class categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(null=False, unique=True, max_length=100)

    def __str__(self):
        return f"{self.category_name}"


# Stores product details
class products(models.Model):
    product_id = models.CharField(primary_key=True, max_length=50)
    product_name = models.CharField(null=False, max_length=255)
    product_price = models.JSONField(null=False, default=dict)
    product_ratings = models.JSONField(null=False, default=dict)
    currency = models.CharField(null=False, max_length=10)
    is_available = models.BooleanField(default=True)
    product_url = models.URLField(null=False)
    product_image_url = models.JSONField(null=True, default=dict)
    product_details = models.JSONField(null=True)
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
    status = {
        '1': 'Active',
        '2': 'Completed',
        '3': 'Cancelled',
    }
    track_id = models.BigAutoField(primary_key=True)
    desired_price = models.DecimalField(null=False, max_digits=19, decimal_places=2)
    last_price = models.DecimalField(null=False, max_digits=19, decimal_places=2)
    tracking_status = models.CharField(max_length=10, choices=status, default='Active')
    scraped_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(user_details, on_delete=models.CASCADE)
    product_id = models.ForeignKey(products, on_delete=models.CASCADE)
    category_id = models.ForeignKey(categories, on_delete=models.CASCADE)


