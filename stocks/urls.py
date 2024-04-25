from django.urls import path

from . import views


urlpatterns = [
    path('', views.stock_list, name="stock-list"),
    path('search/', views.search_stock, name="search-stock"),
    path('create/', views.create_stock, name="create-stock"),
    path('edit/<int:id_stock>', views.edit_stock, name="edit-stock"),
    path('delete/<int:id_stock>', views.delete_stock, name="delete-stock"),
    path('price-quote-history/<int:id_stock>/<int:frequency>', views.price_quote_history, name="price-quote-history")
]