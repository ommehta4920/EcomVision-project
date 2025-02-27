from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('category/', CategoryPage.as_view(), name='categories-page'),
    path('products/',ProductListPage.as_view(), name='products-list-page'),
    path('product-details/', ProductDetailsPage.as_view(), name='product-detail-page'),
    path('comparison/', ProductComparisonPage.as_view(), name='product-comparison-page'),
]