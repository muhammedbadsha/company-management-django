from django.urls import path
from .views import (index, UserRegistrationsView,UserDetailView, UserLoginView)



urlpatterns = [
    path('', index, name= "index"),
    path('registration', UserRegistrationsView.as_view()),
    path('details_view_update/<int:pk>',UserDetailView.as_view()),
    path('user_login', UserLoginView.as_view()),
]
