"""
URL configuration for db_automation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dice/", include('dice.urls')),
    path("game/", include('game.urls')),
    path("player/", include('player.urls')),
    path("car/", include('car.urls')),
    #path("car-registration/", include('car_registration.urls')),
    #path("car-business-pricing/", include('car_business_pricing.urls')),
    path("pandas-basic/", include('pandas_basic.urls')),
    path("excel-basic/", include('excel_basic.urls')),
    path("kakao-oauth/", include('kakao_authentication.urls')),
    path("account/", include('account.urls')),
    path("account-profile/", include('account_profile.urls')),
    path("normalize/", include('normalization.urls')),
    path("game-software/", include('game_software.urls')),
    path("regression/", include('regression.urls')),
    path("authentication/", include('authentication.urls')),
    path("cart/", include('cart.urls')),
    path("payments/", include('payments.urls')),
    path("orders/", include('orders.urls')),
    path("board/", include('board.urls')),
    path("image-gallery/", include('image_gallery.urls')),
    path("blog-post/", include('blog_post.urls')),
]
