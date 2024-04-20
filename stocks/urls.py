from django.urls import path

from . import views


urlpatterns = [
    path('', views.stock_list, name="stock-list"),
    path('create-stock/', views.create_stock, name="create-stock"),
]