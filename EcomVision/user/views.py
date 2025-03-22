import sys
from EcomVision import settings
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
import subprocess
import os

from user.models import *

class HomePage(View):
    def get(self, request):
        return render(request, "home.html")

class SignInPage(View):
    def get(self, request):
        return render(request, "signin.html")

    def post(self, request):
        user_email = request.POST["user_email"]
        user_passwd = request.POST["user_passwd"]

        print("**********", user_email, "\n-*-*-*-", user_passwd)

        if user_details.objects.filter(user_email=user_email, user_passwd=user_passwd).exists():

            try:
                user = user_details.objects.filter(user_email=user_email).first()
                print("User Details :- ", user)

                messages.success(request, "Welcome "+str(user.user_name))

                return redirect("/", {"user_name": user.user_name})

            except:
                print("--------", sys.exc_info())

        else:
            print("---------->>> Your Email or Password is incorrect!")
            messages.error(request, "Your Email isn't registered or Password is incorrect!")
            messages.info(request, "Please try again..")
            return render(request, "signin.html", {"user_email": user_email})



class SignUpPage(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        user_name = request.POST["user_name"]
        user_email = request.POST["user_email"]
        user_passwd = request.POST["user_passwd"]
        user_c_passwd = request.POST["user_c_passwd"]
        # created_at = timezone.now()

        print(f" user_name : {user_name} \n user_email : {user_email} \n user_passwd : {user_passwd} \n user_c_passwd : {user_c_passwd}")

        if user_details.objects.filter(user_email=user_email).exists():
            messages.error(request, "Email already registered!")
            return render(request, "signup.html", {"user_name": user_name, "user_passwd": user_passwd, "user_c_passwd": user_c_passwd})

        if user_passwd != user_c_passwd:
            print("-------- Both password must be same..! --------")
            messages.info(request, "Both password must be same..!")
            return render(request, "signup.html", {"user_name": user_name, "user_email": user_email})

        user = user_details(user_name=user_name, user_email=user_email, user_passwd=user_passwd)

        try:
            user.save()
            messages.success(request, "You are successfully registered...")
            return render(request, "signin.html", {})

        except:
            print("---------", sys.exc_info())

class ForgotPage(View):
    def get(self, request):
        return render(request, "forgot.html")

    def post(self, request):
        user_otp = request.POST["user_otp"]
        user_passwd = request.POST["user_passwd"]
        user_c_passwd = request.POST["user_c_passwd"]

        user_email = 'pshubham8734@gmail.com'

        print("**********", user_otp, "\n-*-*-*-", user_passwd, "\n-*-*-*-", user_c_passwd, "\n-*-*-*-", user_email)

        if user_details.objects.filter(user_email=user_email, user_otp=user_otp).exists():

            if user_passwd != user_c_passwd:
                print("-------- Both password must be same..! --------")
                messages.info(request, "Both password must be same..!")

                return render(request, "forgot.html", {"visibility": True, "user_otp": user_otp})

            try:
                user = user_details.objects.filter(user_email=user_email, user_otp=user_otp)
                user.update(user_passwd=user_passwd)

                print("<<--------- Password has been successfully reset... ---------->>")
                messages.success(request, "Password has been successfully reset...")

                return redirect("/signin")

            except:
                print("--------", sys.exc_info())

        else:
            print("-------- OTP is incorrect! --------")
            messages.error(request, "OTP is incorrect!")

        return render(request, "forgot.html", {"visibility": True, "user_passwd": user_passwd, "user_c_passwd": user_c_passwd})


import random
from django.core.mail import send_mail

class Send_otpPage(View):

    def get(self):
        return redirect("/forgot")

    def post(self, request):
        otp = random.randint(1000, 9999)
        user_email = request.POST["user_email"]

        # request.session['temail'] = user_email
        #
        # print("Session temail :", request.session['temail'])

        if user_details.objects.filter(user_email=user_email).exists():

            try:
                user = user_details.objects.filter(user_email=user_email)
                user.update(user_otp=str(otp))

                subject = "Your EcomVision Portal OTP"
                message = "Dear user, you want to reset your password of your EcomVision account. \n\n Use OTP: " + str(otp) + "\n\nNote: Do not share the OTP with anyone else."
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_email, ]

                send_mail(subject, message, email_from, recipient_list)

                print("**********", subject, "\n-*-*-*-", message, "\n-*-*-*-", email_from, "\n-*-*-*-", recipient_list)

                messages.info(request, "OTP has been sent to your registered email..!")

                return render(request, "forgot.html", {"visibility": True})

            except:
                print("---------", sys.exc_info())
                return render(request, "forgot.html", {})

        else:
            messages.error(request, "Email is not registered!")
            return render(request, "forgot.html", {})


class CategoryPage(View):
    def get(self, request):
        category = categories.objects.all()
        return render(request, "category.html", {"categories": category})

class ProductListPage(View):
    def get(self, request, c_id):
        category = get_object_or_404(categories, category_id=c_id)
        products_list = products.objects.filter(category_id_id = category.category_id)
        return render(request, "product_list.html", {"products": products_list, "category": category})
    
class ProductDetailsPage(View):
    def get(self, request, c_id, p_id):
        # Fetching Product and Category data
        category = get_object_or_404(categories, category_id = c_id)
        c_name = category.category_name[:-1]
        product_data = get_object_or_404(products, product_id = p_id)
        
        # Fetching Latest Price 
        p_price = product_data.product_price
        if p_price:
            last_date = max(p_price.keys())  # Get the last date
            last_price = p_price[last_date]  # Get the price for the last date
        else:
            last_price = "N/A"
            
        # Fetching Data to display in the graphs
        labels = sorted(p_price.keys())
        values = (p_price[date] for date in labels)     
        context = {"chartLabels": labels, "chartValues": [int(value.replace(',', '')) for value in values], "c_name": c_name, "product_data": product_data, "last_price": last_price, "category": category}
        return render(request, "product_details.html", context)
       
class ProductComparisonPage(View):
    def get(self, request):
        category_data = categories.objects.all()
        tv_data = products.objects.filter(category_id = 12)
        laptop_data = products.objects.filter(category_id = 14)
        mobile_data = products.objects.filter(category_id = 13)
        return render(request, "comparison.html", {"category_data": category_data, "tv_data": tv_data, "laptop_data": laptop_data, "mobile_data": mobile_data})

class ScraperPage(View):
    def get(self,request):
        return render(request, "scraper.html")
    
    def post(self, request):
        query = request.POST["query"]

        print("\n ********* query :-"+query+"\n")
        
        # if not query:
        #     messages.error(request, "Please Provide Input")
        #     return redirect("/scraper")
        
        project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../ecom_scraper")

        # Set environment variables for Django
        env = os.environ.copy()
        env["DJANGO_SETTINGS_MODULE"] = "EcomVision.settings"
        env["PYTHONPATH"] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        try:
            subprocess.run(["scrapy", "crawl", "ecom_spider", "-a", f"query={query}"], cwd=project_path, env=env, check=True)
            messages.success(request, f"Scraping completed for: {query}")
        except subprocess.CalledProcessError as e:
            messages.error(request, f"Scrapy encountered an error: {e}")
        return redirect("/")


class ProfilePage(View):
    def get(self, request):
        return (request, 'profile.html')