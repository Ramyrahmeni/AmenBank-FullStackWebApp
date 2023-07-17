from django.urls import path
from . import views
urlpatterns = [
    path('form/',views.form,name='form'),
    path('plus/', views.plus,name='plus'),#urlpatterns = [
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('setprfr/', views.setprfr, name='setprfr'),
    path('setprfrlib/', views.setprfrlib, name='setprfrlib'),
    path('setprfrmail/', views.setprfrmail, name='setprfrmail'),
    path('setprfrsms/', views.setprfrsms, name='setprfrsms'),
    path('setprfrcompteur/', views.setprfrcompteur, name='setprfrcompteur'),
    path('setmail/', views.setmail, name='setmail'),
    path('setinf/', views.setinf, name='setinf'),
    path('security/', views.security, name='security'),

    # Other URL patterns
]