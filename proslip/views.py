from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import DetailView, ListView
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from .models import Profile
from .forms import *
from proslip.filters import ProfileFilter
from django.contrib.auth import get_user_model
from django.views import View
from .script import process_payslip
import os
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, FileResponse
User = get_user_model()
from django.utils import timezone
from django.db import transaction
import uuid
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from PyPDF2 import PdfWriter,PdfReader
import re


# views.py
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models, transaction
from PyPDF2 import PdfReader, PdfWriter
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Payslip, Profile
from .forms import PayslipUploadForm

class DownloadPDFView(View):
    def get(self, request, payslip_id):
        payslip = get_object_or_404(Payslip, id=payslip_id)

        # Set the appropriate response headers for file download
        response = HttpResponse(payslip.file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{payslip.file.name}"'
        return response

def generate_filename(profile, page_num):
    user_username = profile.user.username
    month_year = timezone.now().strftime('%B_%Y')
    filename = f"{user_username}_Payslip_{month_year}_Page_{page_num}.pdf"
    return filename

@transaction.atomic
def process_payslip(pdf_path):
    try:
        pdf = PdfReader(pdf_path)
    except Exception as e:
        # Handle the specific exception for PDF reading error
        print(f"Error reading PDF: {e}")
        return

    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        text_content = page.extract_text()

        ippis_match = re.search(r'(\d{6})', text_content)
        ippis_number = ippis_match.group(1) if ippis_match else None

        if not ippis_number:
            print(f"Skipping page {page_num + 1}: ladaghtno sniffin")
            continue

        try:
            profile = Profile.objects.get(ippis_no=ippis_number)
        except Profile.DoesNotExist:
            print(f"No Profile found for ladaghtno sniffin {ippis_number}")
            continue

        payslip_exists = Payslip.objects.filter(profile=profile).exists()
        payslip_filename = generate_filename(profile, page_num)
        payslip_file_path = os.path.join(settings.MEDIA_ROOT, 'payslips', payslip_filename)

        if not payslip_exists:
            payslip = Payslip(profile=profile)

            # Create a new PDF using PyPDF2 PdfWriter
            pdf_writer = PdfWriter()
            pdf_writer.add_page(page)

            # Save the new PDF to Payslip model    
            with open(payslip_file_path, 'wb') as payslip_file:
                pdf_writer.write(payslip_file)
                payslip.file.name = payslip_file_path
                payslip.save()
            print(f"Payslip created for: {profile.user.get_full_name()} (Page {page_num + 1})")
        else:
            payslip = Payslip.objects.get(profile=profile)
            pdf_writer = PdfWriter()
            pdf_writer.add_page(page)

            # Save the new PDF to Payslip model
            with open(payslip_file_path, 'wb') as payslip_file:
                pdf_writer.write(payslip_file)

            # Assign the file to the Payslip model
            payslip.file.name = payslip_file_path
            payslip.save()

            print(f"Payslip updated for: {profile.user.get_full_name()} (Page {page_num + 1})")

class PayslipUploadView(View):
    template_name = "proslip/upload_payslip.html"

    def get(self, request):
        form = PayslipUploadForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = PayslipUploadForm(request.POST, request.FILES)
        if form.is_valid():
            payslip_file = request.FILES['payslip_file']

            # Save the uploaded payslip file
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_payslip', f'{uuid.uuid4()}_{payslip_file.name}')
            try:
                with FileSystemStorage(location=file_path).open(file_path, 'wb') as destination:
                    for chunk in payslip_file.chunks():
                        destination.write(chunk)
                process_payslip(file_path)
                return redirect('success')
            except Exception as e:
                print(f"Error processing payslip: {e}")
                return HttpResponse("Error processing payslip.")
        else:
            return render(request, self.template_name, {'form': form})

@receiver(post_save, sender=Payslip)
def process_payslip_on_save(sender, instance, created, **kwargs):
    if created:
        process_payslip(instance.file.path)

# class DownloadPDFView(View):
#     def get(self, request, payslip_id):
#         payslip = get_object_or_404(Payslip, id=payslip_id)

#         # Set the appropriate response headers for file download
#         response = FileResponse(open(payslip.file.path, 'rb'))
#         response['Content-Disposition'] = f'attachment; filename="{payslip.file.name}"'
#         return response
    
# class DownloadPDFView(View):
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         if user.is_superuser or hasattr(User, 'profile'):
#             if user.is_superuser:
#                 profile = get_object_or_404(Profile, user__username=kwargs['username'])
#             else:
#                 profile = user.profile

#             try:
#                 payslip = Payslip.objects.get(profile=profile)
#                 if payslip.file:
#                     file_path = payslip.file.path

#                     if file_path:
#                         print(f"File path: {file_path}")  # Add this line to print the file path

#                         response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
#                         response['Content-Disposition'] = f"attachment; filename=\"{payslip.profile.ippis_no}_payslip.pdf\""
#                         return response
#                     else:
#                         return HttpResponse("Payslip file path is None")
#                 else:
#                     return HttpResponse("Payslip has no associated file")
#             except Payslip.DoesNotExist:
#                 return HttpResponse("Payslip not found")
#         else:
#             return HttpResponse("User has no profile")


def success(request):
    return render(request,'success.html')

def log_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated,login_url=redirect_to)(view_function)

def reg_required(view_function, redirect_to=None):
    if redirect_to is None:
        redirect_to = '/'
    return user_passes_test(lambda u: not u.is_authenticated or u.is_superuser,login_url=redirect_to)(view_function)

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return render(request,'access_denied.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def index(request):
    return render(request, 'index.html')


@method_decorator(log_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name='login.html'
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('list')
        else:
            return reverse_lazy('profile_page',args=[self.request.user.username])


@method_decorator(login_required, name='dispatch')
class CustomLogoutView(LogoutView):
    template_name='logged_out.html'


@method_decorator(reg_required, name='dispatch')
class UserRegistrationView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if form.is_valid():
            response = super().form_valid(form)
            user = User.objects.get(username=form.cleaned_data['username'])
            profile_instance = Profile(user=user)
            profile_instance.save()
            messages.success(self.request, f"Registration for {user.get_full_name()} was successful")
            return response
        else:
            print("Form errors:", form.errors)
            return self.form_invalid(form)


class DocView(UpdateView):
    model = User
    template_name = 'doc.html'
    form_class = UserForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profileform'] = ProfileForm(instance=self.object.profile)
        return context

    def form_valid(self, form):
        userform=UserForm(self.request.POST, instance=self.object)
        profileform = ProfileForm(self.request.POST, instance=self.object.profile)

        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(self.request, f'Documentation was successful {self.request.user.last_name}')
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, 'Please correct the errors')
            return self.form_invalid(form)


# @method_decorator(login_required(login_url='login'), name='dispatch')
# class UpdateUserView(UpdateView):
#     model=User
#     template_name= 'proslip/update_user.html'
#     form_class=UserForm
#     success_url=reverse_lazy('profile_page')

#     def get_success_url(self):
#         return reverse_lazy('profile_page', kwargs={'username': self.object.username})

#     def form_valid(self,form):
#         if form.is_valid():
#             form.save()
#             messages.success(self.request, 'User Information Updated Successfully')
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_invalid(self,form):
#         messages.error(self.request,'Please Correct the error')
#         return self.render_to_response(self.get_context_data(form=form))



# @method_decorator(login_required(login_url='login'), name='dispatch')
# class UpdateProfileView(UpdateView):
#     model=Profile
#     template_name = 'proslip/update_profile.html'
#     form_class=ProfileForm
#     success_url=reverse_lazy('profile_page')

#     def get_success_url(self):
#         return reverse_lazy('profile_page', kwargs={'username': self.object.user})

#     def form_valid(self,form):
#         if form.is_valid():
#             form.save()
#             messages.success(self.request, 'User Information Updated Successfully')
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)

#     def form_invalid(self,form):
#         messages.error(self.request,'Please Correct the error')
#         return self.render_to_response(self.get_context_data(form=form))



@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfilePageView(DetailView):
    model=Profile
    template_name='proslip/profile_page.html'
    slug_field = 'user__username'  # Specify the field to use for the slug
    slug_url_kwarg = 'username'  # Specify the parameter name from the URL

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)

        if self.request.user.is_superuser:
            username_from_url=self.kwargs.get('username')
            context['profile']=get_object_or_404(Profile,user__username=username_from_url)
        else:
            context['profile']=self.request.user.profile

        payslips=Payslip.objects.filter(profile=context['profile'])
        context['payslips']=payslips
        context['payslip_ids']=[payslip.id for payslip in payslips]
        return context


@method_decorator(superuser_required,name='dispatch')
class StaffListView(ListView):
    model=Profile
    template_name = 'proslip/stafflist.html'
    context_object_name = 'po'
    paginate_by = 10

    def get_queryset(self):
        return Profile.objects.all().order_by('dept_or_unit')


@superuser_required
def search(request):
    profilefilter=ProfileFilter(request.GET, queryset=Profile.objects.all().order_by('dept_or_unit'))    
    context = {'profilefilter': profilefilter}
    return render(request, 'proslip/search.html', context)