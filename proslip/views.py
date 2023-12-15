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
from django.http import Http404
User = get_user_model()


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
            return render(request,'access-denied.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def index(request):
    return render(request, 'index.html')


@method_decorator(log_required, name='dispatch')
class CustomLoginView(LoginView):
    template_name='login.html'
    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('index')
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



@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateUserView(UpdateView):
    model=User
    template_name= 'staff/update-user.html'
    form_class=UserForm
    success_url=reverse_lazy('profile_page')

    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={'username': self.object.username})

    def form_valid(self,form):
        if form.is_valid():
            form.save()
            messages.success(self.request, 'User Information Updated Successfully')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Please Correct the error')
        return self.render_to_response(self.get_context_data(form=form))



@method_decorator(login_required(login_url='login'), name='dispatch')
class UpdateProfileView(UpdateView):
    model=Profile
    template_name = 'staff/update-profile.html'
    form_class=ProfileForm
    success_url=reverse_lazy('profile_page')

    def get_success_url(self):
        return reverse_lazy('profile_page', kwargs={'username': self.object.user})

    def form_valid(self,form):
        if form.is_valid():
            form.save()
            messages.success(self.request, 'User Information Updated Successfully')
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self,form):
        messages.error(self.request,'Please Correct the error')
        return self.render_to_response(self.get_context_data(form=form))



@method_decorator(login_required(login_url='login'), name='dispatch')
class ProfilePageView(DetailView):
    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                username_from_url = kwargs.get('username')
                profile = get_object_or_404(Profile, user__username=username_from_url)
            else:
                profile = request.user.profile        
        except Http404:
            profile=None
        context = {'profile': profile}
        return render(request, 'staff/profile_page.html', context)



@method_decorator(superuser_required,name='dispatch')
class StaffListView(ListView):
    model=Profile
    template_name = 'proslip/staff_list.html'
    context_object_name = 'po'
    paginate_by = 10

    def get_queryset(self):
        return Profile.objects.all().order_by('dept_or_unit')


@method_decorator(superuser_required,name='dispatch')
def item_report(request):
    profilefilter=ProfileFilter(request.GET, queryset=Profile.objects.all().order_by('dept_or_unit'))    
    context = {'profilefilter': profilefilter}
    return render(request, 'proslip/search.html', context)