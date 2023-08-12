""" core app URL Configuration """

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('addItem/', views.addItem, name='addItem'),
    path("create_supplier", views.create_supplier, name="add_supplier"),
]