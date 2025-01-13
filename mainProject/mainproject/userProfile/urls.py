from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.Profile,name = 'profile'),
    path('updateInfo/',views.updateInfo,name = 'updateInfo'),
    path('get_codeforces_submissions/',views.get_codeforces_submissions,name='get_codeforces_submissions'),
]
