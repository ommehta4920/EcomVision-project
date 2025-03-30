import sys
from EcomVision import settings
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
import subprocess
import os
import logging

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
                # user = user_details.objects.filter(user_email=user_email).first()

                user_data = get_object_or_404(user_details, user_email=user_email)
                print("User Details :- ", user_data)

                messages.success(request, "Welcome "+user_data.user_name)

                return redirect("/", {"user_data": user_data})

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

        print("\n **---- Product_data : ", product_data, "\n")
        
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
    def get(self, request, c_id = None):
        category_data = categories.objects.all()
        if c_id:
            logger = logging.getLogger(__name__)
            logger.debug(f"Category ID received: {c_id}")
            try:
                categoryData = categories.objects.get(category_id = c_id)
                product_data = products.objects.filter(category_id=categoryData.category_id)
                print(f"Category ID: {c_id}, Products Found: {product_data.count()}")

                if not product_data.exists():  # Ensure products exist
                    return JsonResponse({'products_detail': [], 'message': 'No products found'})
                product_list = [{'product_id': p.product_id, 'product_name': p.product_name, 'product_price': p.product_price, 'product_rating': p.product_ratings, 'product_image': p.product_image_url[0], 'product_details': p.product_details} for p in product_data]
                # print(product_list)
                return JsonResponse({'products_detail': product_list})
            except categories.DoesNotExist:
                return HttpResponseNotFound(JsonResponse({'error': 'category not found.'}))
        return render(request, "product_comparison.html", { "category_data": category_data, 'products_detail': []})

class ProfilePage(View):
    def get(self, request):
        userid = request.session.get("user_id")
        if not userid:
            return redirect("/signin")
        else:
            user_data = user_details.objects.get(user_id = userid)
        
        return render(request, 'profile.html', {"user_data": user_data})

    def post(self, request):
        user_id = request.session.get("user_id")

        if not user_id:
            return redirect("/signin")

        # Get updated data from form
        name = request.POST.get("name")
        email = request.POST.get("email")

        # Update user details in the database
        user = user_details.objects.get(user_id=user_id)
        user.user_name = name
        user.user_email = email
        user.save()

        # Update session with new data
        request.session["user_name"] = name
        request.session["user_email"] = email

        messages.success(request, "Profile updated successfully!")
        return redirect("/profile")

def logout_user(request):
    request.session.flush()
    return redirect("/")