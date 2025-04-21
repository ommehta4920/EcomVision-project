import sys
from EcomVision import settings
from django.contrib import messages
from django.views import View
from user.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, JsonResponse, HttpResponseRedirect
import logging
from django.contrib.auth import update_session_auth_hash, logout
import requests
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.

class HomePage(View):
    def get(self, request):
        raw_products = products.objects.filter(is_available=True).order_by('-scraped_at')[:20]
        print("Total available products:", raw_products.count())
        latest_products = []
        for product in raw_products:
            price_data = product.product_price  # e.g., {"2025-04-05": "14,520"}
            if isinstance(price_data, dict) and price_data:
                latest_date = sorted(price_data.keys())[-1]  # get latest date
                latest_price = price_data[latest_date]
            else:
                latest_price = "N/A"

            latest_products.append({
                'product_id': product.product_id,
                'name': product.product_name,
                'price': latest_price,
                'currency': product.currency,
                'image_url': product.product_image_url[0],
                'url': product.product_url,
                'category_id': product.category_id.category_id
            })

        return render(request, "home.html", {'latest_products': latest_products})


class SignInPage(View):
    def get(self, request):
        return render(request, "signin.html")

    def post(self, request):
        user_email = request.POST["user_email"]
        user_passwd = request.POST["user_passwd"]

        print("**********", user_email, "\n-*-*-*-", user_passwd)

        if user_details.objects.filter(user_email=user_email, user_passwd=user_passwd).exists():

            try:
                # user_data = user_details.objects.filter(user_email=user_email).first()

                user_data = get_object_or_404(user_details, user_email=user_email)
                request.session["user_id"] = user_data.user_id
                print("User Details :- ", user_data)

                messages.success(request, "👋 Login Successful, Welcome " + user_data.user_name + "! 😊")
                return redirect("/profile")
                # return render(request, "home.html", {"user_data": user_data})

            except:
                print("--------", sys.exc_info())

        else:
            print("---------->>> Your Email or Password is incorrect!")
            messages.error(request, "❌ Your Email isn't registered or Password is incorrect!")
            messages.info(request, "ℹ Please try again..")
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

        print(
            f" user_name : {user_name} \n user_email : {user_email} \n user_passwd : {user_passwd} \n user_c_passwd : {user_c_passwd}")

        if user_details.objects.filter(user_email=user_email).exists():
            messages.error(request, "❌ Email already registered!")
            return render(request, "signup.html",
                          {"user_name": user_name, "user_passwd": user_passwd, "user_c_passwd": user_c_passwd})

        if user_passwd != user_c_passwd:
            print("-------- Both password must be same..! --------")
            messages.info(request, "ℹ Both password must be same..!")
            return render(request, "signup.html", {"user_name": user_name, "user_email": user_email})

        user = user_details(user_name=user_name, user_email=user_email, user_passwd=user_passwd)

        try:
            user.save()
            messages.success(request, "✔ You are successfully registered...")
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
        user_email = request.session["t_email"]

        print("**********", user_otp, "\n-*-*-*-", user_passwd, "\n-*-*-*-", user_c_passwd, "\n-*-*-*-", user_email)

        if user_details.objects.filter(user_email=user_email, user_otp=user_otp).exists():

            if user_passwd != user_c_passwd:
                print("-------- Both password must be same..! --------")
                messages.info(request, "ℹ Both password must be same..!")

                return render(request, "forgot.html", {"visibility": True, "user_otp": user_otp})

            try:
                user = user_details.objects.filter(user_email=user_email, user_otp=user_otp)
                user.update(user_passwd=user_passwd)

                print("<<--------- Password has been successfully reset... ---------->>")
                messages.success(request, "✔ Password has been successfully reset...")

                return redirect("/signin")

            except:
                print("--------", sys.exc_info())

        else:
            print("-------- OTP is incorrect! --------")
            messages.error(request, "❌ OTP is incorrect!")

        return render(request, "forgot.html",
                      {"visibility": True, "user_passwd": user_passwd, "user_c_passwd": user_c_passwd})


import random
from django.core.mail import send_mail


class Send_otpPage(View):

    def get(self):
        return redirect("/forgot")

    def post(self, request):
        otp = random.randint(1000, 9999)
        user_email = request.POST["user_email"]

        request.session["t_email"] = user_email

        if user_details.objects.filter(user_email=user_email).exists():

            try:
                user = user_details.objects.filter(user_email=user_email)
                user.update(user_otp=str(otp))

                subject = "Your EcomVision Portal OTP"
                message = "Dear user, you want to reset your password of your EcomVision account. \n\n Use OTP: " + str(
                    otp) + "\n\nNote: Do not share the OTP with anyone else."
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user_email, ]

                send_mail(subject, message, email_from, recipient_list)

                print("**********", subject, "\n-*-*-*-", message, "\n-*-*-*-", email_from, "\n-*-*-*-", recipient_list)

                messages.info(request, "ℹ OTP has been sent to your registered email..!")

                return render(request, "forgot.html", {"visibility": True})

            except:
                print("---------", sys.exc_info())
                return render(request, "forgot.html", {})

        else:
            messages.error(request, "❌ Email is not registered!")
            return render(request, "forgot.html", {})


class CategoryPage(View):
    def get(self, request):
        category = categories.objects.all()
        return render(request, "category.html", {"categories": category})


class ProductListPage(View):
    def get(self, request, c_id):
        category = get_object_or_404(categories, category_id=c_id)
        products_list = products.objects.filter(category_id_id=category.category_id)
        
        # Process products to include latest price
        processed_products = []
        prices = []
        
        for product in products_list:
            latest_price = None
            if product.product_price:
                last_date = max(product.product_price.keys())
                latest_price = product.product_price[last_date]
                # Remove commas and convert to float for price ranges
                price_float = float(latest_price.replace(',', ''))
                prices.append(price_float)
            
            processed_products.append({
                'product': product,
                'latest_price': latest_price,
                'price_float': price_float if latest_price else 0
            })
        
        # Calculate price ranges
        price_ranges = []
        if prices:
            min_price = min(prices)
            max_price = max(prices)
            
            # Create 5 price ranges
            range_size = (max_price - min_price) / 5
            for i in range(5):
                range_min = min_price + (i * range_size)
                range_max = min_price + ((i + 1) * range_size)
                # Round to nearest 1000 for cleaner ranges
                range_min = round(range_min / 1000) * 1000
                range_max = round(range_max / 1000) * 1000
                price_ranges.append({
                    'min': range_min,
                    'max': range_max
                })
        
        context = {
            "products": processed_products,
            "category": category,
            "price_ranges": price_ranges
        }
        return render(request, "product_list.html", context)


class ProductDetailsPage(View):
    def get(self, request, c_id, p_id):
        # Fetching Product and Category data
        category = get_object_or_404(categories, category_id=c_id)
        c_name = category.category_name[:-1]
        product_data = get_object_or_404(products, product_id=p_id)

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
        context = {"chartLabels": labels, "chartValues": [int(value.replace(',', '')) for value in values],
                   "c_name": c_name, "product_data": product_data, "last_price": last_price, "category": category}

        return render(request, "product_details.html", context)

    def post(self, request, c_id, p_id):

        category = get_object_or_404(categories, category_id=c_id)
        c_name = category.category_name[:-1]
        product_data = get_object_or_404(products, product_id=p_id)

        # <----- Not required because of session condition on button ----->
        userId = request.session.get("user_id")
        if not userId:
            return JsonResponse({"error": "❌ User not authenticated"}, status=403)
        # <----- Not required ----->

        user = get_object_or_404(user_details, user_id=userId)

        # Fetching Latest Price
        p_price = product_data.product_price
        if p_price:
            last_date = max(p_price.keys())  # Get the last date
            last_price = p_price[last_date]  # Get the price for the last date
        else:
            last_price = "N/A"

        # Get user input for desired price
        desired_price = request.POST.get("desiredPrice")

        # <----- Not required because of HTML required Field ----->
        if not desired_price:
            return JsonResponse({"error": "❌ Desired price is required"}, status=400)
        # <---- Not required ----->

        existing_tracking = price_track.objects.filter(
            user_id=user,
            product_id=product_data,
            desired_price=desired_price,
            tracking_status=1
        ).exists()

        if existing_tracking:
            messages.info(request, 'ℹ This price tracking is already exists! 🔁')
            return redirect("/profile")
        else:
            tracking_entry = price_track.objects.create(
                user_id=user,  # Retrieved from session
                product_id=product_data,
                category_id=category,
                desired_price=desired_price,
                last_price=last_price,
                tracking_status='1'  # Active
            )

            tracking_entry.save()
            messages.success(request, '✔ Price tracking has been successfully created! 🛠️')
            return redirect("/profile")

        labels = sorted(p_price.keys())
        values = (p_price[date] for date in labels)
        context = {"chartLabels": labels, "chartValues": [int(value.replace(',', '')) for value in values],
                   "c_name": c_name, "product_data": product_data, "last_price": last_price, "category": category}

        return render(request, "product_details.html", context)


class ProductDetailsPageComparison(View):
    def get(self, request, c_id=None, p_id=None, to_compare=False):
        category_data = categories.objects.all()
        if to_compare and p_id and c_id:
            try:
                selected_category = categories.objects.get(category_id=c_id)
                product_data = products.objects.filter(category_id=c_id)
                print(
                    f"Category ID: {c_id}, Products Found: {product_data.count()}")

                # if not product_data.exists():  # Ensure products exist
                #     return JsonResponse({'products_detail': [], 'message': 'No products found'})

                product_list = [
                    {'product_id': p.product_id, 'product_name': p.product_name, 'product_price': p.product_price,
                     'product_rating': p.product_ratings, 'product_image': p.product_image_url[0],
                     'product_details': p.product_details} for p in product_data]
                print(product_list)

                selected_product = next((p_dict for p_dict in product_list if str(p_dict["product_id"]) == str(p_id)),
                                        None)

                return render(request, "comparison.html",
                              {"category_data": category_data, "selected_category_id": c_id,
                               "products_detail": product_list,
                               "selected_product": selected_product})  # To get products of particular category
            except categories.DoesNotExist:
                messages.error(request, "❌ Sorry category not found.")
        return render(request, "comparison.html",
                      {"category_data": category_data, "selected_category_id": None, 'products_detail': [],
                       "selected_product": None})


class ProductComparisonPage(View):
    def get(self, request, c_id=None):
        category_data = categories.objects.all()
        if c_id:
            logger = logging.getLogger(__name__)
            logger.debug(f"Category ID received: {c_id}")
            try:
                categoryData = categories.objects.get(category_id=c_id)
                product_data = products.objects.filter(category_id=categoryData.category_id)
                print(f"Category ID: {c_id}, Products Found: {product_data.count()}")

                if not product_data.exists():  # Ensure products exist
                    return JsonResponse({'products_detail': [], 'message': 'No products found'})
                product_list = [
                    {'product_id': p.product_id, 'product_name': p.product_name, 'product_price': p.product_price,
                     'product_rating': p.product_ratings, 'product_image': p.product_image_url[0],
                     'product_details': p.product_details} for p in product_data]
                print(product_list)
                return JsonResponse({'products_detail': product_list})  # To get products of particular category
            except categories.DoesNotExist:
                messages.error(request, "❌ Sorry category not found.")
                return HttpResponseNotFound(JsonResponse({'error': '❌ Sorry category not found.'}))
                # return render(request, "comparison.html")
        return render(request, "comparison.html", {"category_data": category_data, 'products_detail': []})


class SetPasswordView(View):
    def get(self, request):
        return render(request, "set_password.html")

    def post(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("/signin")

        password = request.POST.get("user_passwd")
        confirm = request.POST.get("user_c_passwd")

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect("/set-password")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("/set-password")

        user = user_details.objects.get(user_id=user_id)
        user.user_passwd = password
        user.save()

        messages.success(request, "Password set successfully.")
        return redirect("/profile")


class ProfilePage(View):
    def get(self, request):
        userid = request.session.get("user_id")
        if not userid:
            return redirect("/signin")

        user_data = user_details.objects.get(user_id=userid)

        if not user_data.user_passwd:
            return redirect("/set-password")

        try:
            price_track_details = price_track.objects.select_related('product_id').filter(user_id=userid)
            print("user_data :", user_data)

            response = render(request, 'profile.html',
                              {"user_data": user_data, "price_track_details": price_track_details})
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

            return response
        except price_track.DoesNotExist:
            price_track_details = None
            response = render(request, 'profile.html',
                              {"user_data": user_data, "price_track_details": price_track_details})
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'

            return response

    def post(self, request):
        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("/signin")

        user = user_details.objects.get(user_id=user_id)

        name = request.POST.get("name")
        email = request.POST.get("email")

        user.user_name = name
        user.user_email = email
        user.save()

        # Update session with new data
        request.session["user_name"] = name
        request.session["user_email"] = email

        messages.success(request, "✔ Profile updated successfully!")
        return redirect("/profile")


class logout_user(View):
    def get(self, request):
        request.session.pop("t_email", None)
        logout(request)
        response = HttpResponseRedirect('/signin')
        response.delete_cookie('sessionid')
        return response

    def revoke_google_token(token):
        url = 'https://accounts.google.com/o/oauth2/revoke'
        params = {'token': token}
        response = requests.get(url, params=params)
        return response.status_code == 200


class AboutUs(View):
    def get(self, request):
        return render(request, "aboutus.html")


class ContactUs(View):
    def get(self, request):
        if request.session.get("user_id"):
            userId = request.session.get("user_id")
            user = get_object_or_404(user_details, user_id=userId)
            return render(request, "contactus.html", {'user': user})

        return render(request, "contactus.html")

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        print("/*--*//*--*//*--*// name |", name, "\n/*--*//*--*//*--*// email |", email,
              "\n/*--*//*--*//*--*// message |", message, "\n")

        cont_data = contact_us(cont_name=name, cont_email=email, message=message)

        try:
            cont_data.save()

            subject = 'Contact message from EcomVision'
            message = f'From {name}\n\nSender Mail ID: {email}\n\nMessage:           {message}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]

            send_mail(subject, message, email_from, recipient_list)

            print("**********", subject, "\n-*-*-*-", message, "\n-*-*-*-", email_from, "\n-*-*-*-", recipient_list)

            messages.success(request, "✔ Your message has been delivered successfully...")
            print("-*-*-*-**-**-*-**-*-*-*- Email send Successfully using :- ", email)
            return redirect("/contactus")

        except:
            print("---------", sys.exc_info())

        return redirect("/contactus")

def calculate_price_ranges(products):
    if not products:
        return []
    
    # Get all prices
    prices = [product.last_price for product in products if product.last_price is not None]
    if not prices:
        return []
    
    min_price = min(prices)
    max_price = max(prices)
    
    # Calculate number of ranges (5 ranges for better distribution)
    num_ranges = 5
    range_size = (max_price - min_price) / num_ranges
    
    # Create price ranges
    price_ranges = []
    for i in range(num_ranges):
        range_min = min_price + (i * range_size)
        range_max = min_price + ((i + 1) * range_size)
        # Round to nearest 1000 for cleaner ranges
        range_min = round(range_min / 1000) * 1000
        range_max = round(range_max / 1000) * 1000
        price_ranges.append({
            'min': range_min,
            'max': range_max
        })
    
    return price_ranges

def product_list(request, category_id):
    category = categories.objects.get(category_id=category_id)
    products = products.objects.filter(category_id=category_id)
    
    # Calculate dynamic price ranges
    price_ranges = calculate_price_ranges(products)
    
    context = {
        'category': category,
        'products': products,
        'price_ranges': price_ranges
    }
    return render(request, 'product_list.html', context)

class GetPriceTracking(View):
    def get(self, request, id):
        try:
            print(f"Fetching price tracking data for ID: {id}")
            price_track_data = price_track.objects.get(id=id)
            print(f"Found price tracking data: {price_track_data}")
            
            data = {
                'product_name': price_track_data.product_id.product_name,
                'desired_price': price_track_data.desired_price,
                'tracking_status': price_track_data.tracking_status
            }
            print(f"Returning data: {data}")
            return JsonResponse(data)
        except price_track.DoesNotExist:
            print(f"Price tracking with ID {id} not found")
            return JsonResponse({'error': 'Price tracking not found'}, status=404)
        except Exception as e:
            print(f"Error fetching price tracking data: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

def delete_price_track(request, pk):
    print(pk)
    try:
        track = price_track.objects.get(track_id = pk)
    except price_track.DoesNotExist:
        messages.error(request, "Track not found or you don't have permission.")
        return redirect('/profile')

    track.delete()
    messages.success(request, "✔ Record deleted successfully!")
    return redirect('/profile')
