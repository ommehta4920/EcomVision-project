from django.shortcuts import render, redirect
from django.views import View
# from .models import user_details
from django.contrib import messages
from django.http import JsonResponse

class HomePage(View):
    def get(self, request):
        return render(request, "home.html")
    
class CategoryPage(View):
    def get(self, request):
        return render(request, "category.html")

class ProductListPage(View):
    def get(self, request):
        return render(request, "product_list.html")
    
class ProductDetailsPage(View):
    def get(self, request):
        return render(request, "product_details.html")
       
class ProductComparisonPage(View):
    def get(self, request):
        return render(request, "comparison.html")