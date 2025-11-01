from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # اطمینان از وجود این خط
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('access-denied/', views.access_denied, name='access_denied'),
]