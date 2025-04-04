from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home-page'),
    path('category/', CategoryPage.as_view(), name='categories-page'),
    path('category/<int:c_id>/', ProductListPage.as_view(), name='products-list-page'),
    path('category/<int:c_id>/<str:p_id>/', ProductDetailsPage.as_view(), name='product-detail-page'),
    path('comparison/', ProductComparisonPage.as_view(), name='product-comparison-page'),
    # path('comparison/category/', CategoryPage.as_view(), name='product-comparison-page'),
    # path('comparison/<int:c_id>', ProductComparisonPage.as_view(), name='product-comparison-page-with-id'),
    # path('comparison/<int:c_id>/<str:p_id>/', ProductComparisonPage.as_view(), name='product-comparison-page-with-id'),
    path('signin/', SignInPage.as_view(), name='signin-page'),
    path('signup/', SignUpPage.as_view(), name='signup-page'),
    path('scraper/', ScraperPage.as_view(), name='scraper-page'),
    path('profile/', ProfilePage.as_view(), name='profile-page'),
    path('forgot/', ForgotPage.as_view(), name='forgot-page'),
    path('send_otp/', Send_otpPage.as_view(), name='send_otp-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)