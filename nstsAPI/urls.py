from django.contrib import admin
from django.urls import path
from payment import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.homepage, name='index'),
    path('updateamount', views.updateamount),
    path('paymenthandler270/', views.paymenthandler270),
    path('paymenthandler360/', views.paymenthandler360),
    path('admin/', admin.site.urls)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
