from django.urls import path
from . import views
urlpatterns = [
    path('form/',views.form,name='form'),
    path('plus/', views.plus,name='plus'),
]