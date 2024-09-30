from django.urls import path
from .views import (index, UserRegistrationsView,UserDetailView, UserLoginView, PasswordResetView,passwordResetSendRequestView)



urlpatterns = [
    path('', index, name= "index"),
    path('registration', UserRegistrationsView.as_view()),
    path('details_view_update/<int:pk>',UserDetailView.as_view()),
    path('user_login', UserLoginView.as_view()),
    path("password-reset-email-request",passwordResetSendRequestView.as_view(),name='password-reset-request'),
    path('password-reset/<uidb64>/<token>/', PasswordResetView.as_view(), name="password-reset")
]
