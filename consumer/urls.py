from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdrawal/', views.withdraw, name='withdrawal'),
]