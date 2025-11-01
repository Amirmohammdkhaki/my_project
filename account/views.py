from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

class SignupView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'ثبت‌نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.')
        return response

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        # اگر پارامتر next وجود دارد، به آن آدرس هدایت شود
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('post_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'خوش آمدید {form.get_user().username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'نام کاربری یا رمز عبور اشتباه است.')
        return self.render_to_response(self.get_context_data(form=form))

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'شما با موفقیت خارج شدید.')
        return super().dispatch(request, *args, **kwargs)

def access_denied(request):
    return render(request, 'account/access_denied.html', status=403)