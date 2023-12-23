from django.urls import path, include
from .views import CustomLoginView, ProfilePageView, UserRegistrationView, CustomLogoutView, StaffListView,DocView, PayslipUploadView, DownloadPDFView, PDFView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('upload-payslip/', PayslipUploadView.as_view(), name='upload_payslip'),
    path('download-pdf/<int:payslip_id>/', DownloadPDFView.as_view(), name='download_pdf'),
    path('view-pdf/<int:payslip_id>/', PDFView.as_view(), name='view_pdf'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('documentation/<int:pk>/', DocView.as_view(), name='doc'),
    path('profile/<str:username>/',ProfilePageView.as_view(), name='profile_page'),
    # path('update-user/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
    # path('update-profile/<int:pk>/',UpdateProfileView.as_view(), name='update_profile'),
    path('stafflist/',StaffListView.as_view(), name='list'),
    path('search/',views.search, name='search'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('django.contrib.auth.urls')),
]
