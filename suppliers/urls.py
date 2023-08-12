from django.urls import path
from . import views


urlpatterns = [
    path("", views.suppliers, name="suppliers"),
    path("create_supplier", views.create_supplier, name="add_supplier"),
    path('update_supplier/<str:pk>', views.update_supplier, name="update_supplier"),
    path('delete_supplier/<str:pk>', views.delete_supplier, name="delete_supplier"),
    path('export_to_csv', views.export_to_csv, name='export_to_csv'),
]