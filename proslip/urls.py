from django.urls import path, include
from .views import CustomLoginView, ProfilePageView, UserRegistrationView, CustomLogoutView, UpdateUserView, UpdateProfileView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('profile/<str:username>/',ProfilePageView.as_view(), name='profile_details'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('update-profile/<int:pk>/',UpdateProfileView.as_view(), name='update_profile'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]
