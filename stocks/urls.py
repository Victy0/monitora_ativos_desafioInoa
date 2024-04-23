from django.urls import path

from . import views


urlpatterns = [
    path('', views.stock_list, name="stock-list"),
    path('search/', views.search_stock, name="search-stock"),
    path('create/', views.create_stock, name="create-stock"),
    path('edit/<int:id_stock>', views.edit_stock, name="edit-stock")
]