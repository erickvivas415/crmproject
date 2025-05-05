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
    path('password-reset/', views.custom_password_reset_request, name='custom_password_reset'),
    path('reset/<uidb64>/<token>/', views.custom_password_reset_confirm, name='custom_password_reset_confirm'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('member/<int:id>/', views.member_profile, name='member_profile'),  # This should match the link in your template


]