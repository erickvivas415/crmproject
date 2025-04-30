from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('resumeboard/', views.resumeboard, name='resumeboard'),
    path('login_user/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('search_members/', views.search_members, name='search_members'),
]