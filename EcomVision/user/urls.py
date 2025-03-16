from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('signup/', SignUpPage.as_view(), name='signup-page'),
    path('signin/', SignInPage.as_view(), name='signin-page'),
    path('send_otp/', Send_otpPage.as_view(), name='send_otp-page'),
    path('forgot/', ForgotPage.as_view(), name='forgot-page'),
    path('category/', CategoryPage.as_view(), name='categories-page'),
    path('products/',ProductListPage.as_view(), name='products-list-page'),
    path('product-details/', ProductDetailsPage.as_view(), name='product-detail-page'),
    path('comparison/', ProductComparisonPage.as_view(), name='product-comparison-page'),
    path('scraper/', ScraperPage.as_view(), name='scraper-page'),
]