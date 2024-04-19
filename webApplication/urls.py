from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('create-user/', views.createUser, name="create-user"),
    path('stock-list/', views.stockList, name="stock-list")
]