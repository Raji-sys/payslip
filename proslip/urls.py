from django.urls import path, include
from .views import CustomLoginView, ProfilePageView, UserRegistrationView, CustomLogoutView, UpdateUserView, UpdateProfileView, StaffListView,DocView, PayslipUploadView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('upload-payslip/', PayslipUploadView.as_view(), name='upload_payslip'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('documentation/<int:pk>/', DocView.as_view(), name='doc'),
    path('profile/<str:username>/',ProfilePageView.as_view(), name='profile_page'),
    path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    path('update-profile/<int:pk>/',UpdateProfileView.as_view(), name='update_profile'),
    path('stafflist/',StaffListView.as_view(), name='list'),
    path('search/',views.search, name='search'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]
