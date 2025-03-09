from django.db import models

# Create your models here.

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(null=False, max_length=50)
    user_email = models.EmailField(null=False, unique=True)
    user_passwd = models.CharField(null=False, max_length=20)
    user_otp = models.CharField(null=True, max_length=10)
    created_at = models.DateTimeField(null=False)

    class Meta:
        db_table = "users"
