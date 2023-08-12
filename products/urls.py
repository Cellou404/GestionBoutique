from django.urls import path

from products import views
from .views import DeleteItem

urlpatterns = [
    path('stock/', views.stock, name='stock'),
    path('add_item/', views.add_item, name='add_item'),
    path('addItem/', views.addItem, name='addItem'),
    path('update_item/<str:pk>', views.update_item, name='update_item'),
    path('delete_item/<str:pk>', views.delete_item, name='delete_item'),
    path('delete/<str:pk>', DeleteItem.as_view(), name='delete'),
    path('details_item/<str:pk>', views.details_item, name='view_item'),
    path('issue_item/<str:pk>', views.issue_items, name="issue_item"),
    path('receive_item/<str:pk>', views.receive_items, name="receive_item"),
    path('reorder_level/<str:pk>', views.reorder_level, name="reorder_level"),
    path('update_quantity/<str:pk>', views.update_quantity, name="update_quantity"),
    path('sale_history/', views.sale_history, name="sale_history"),
    path('supply_history/', views.supply_history, name="supply_history"),
    path('export_stock_to_csv', views.export_stock_to_csv, name='export_stock_to_csv'),
]