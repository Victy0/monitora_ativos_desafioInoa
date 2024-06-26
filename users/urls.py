from django.urls import path

from . import views


urlpatterns = [
    path('', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('create-user/', views.create_user, name="create-user"),
    path('edit-user/', views.edit_user, name="edit-user"),
    path('password-reset/', views.password_reset, name="password-reset")
]