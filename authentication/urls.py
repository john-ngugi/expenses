from django.urls import path 

from .views import registrationView,UsernameValidationView,EmailValidationView,LoginView,LogoutView

from django.views.decorators.csrf import csrf_exempt

urlpatterns=[
    path('register/',registrationView.as_view(),name='register'),
    path('login',LoginView.as_view(),name='login'),
    path('validate-username',csrf_exempt(UsernameValidationView.as_view()),name='validate username'),
    path('validate-email',csrf_exempt(EmailValidationView.as_view()),name='validate email'),
    path('logout',LogoutView.as_view(),name='logout'),
]