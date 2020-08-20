from django.conf.urls import url
from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^buynow$', views.buynow),
    url(r'^cart$', views.cart),
    url(r'^addToCart/(?P<product_id>\d+)$', views.addToCart),
    url(r'^delete_item/(?P<product_id>\d+)$', views.delete_item),
    url(r'^ourstory$', views.ourstory),
    url(r'^faq$', views.faq),
    url(r'^contactus$', views.contactus),
    url(r'^checkout$', views.checkout),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    path('charge', views.charge, name="charge"),
    path('success/<str:args>/', views.successMsg, name="success"),
    #path('stripe/<str:args>/', views.successMsg, name="success"),
    path('accounts/', include('allauth.urls')),

]