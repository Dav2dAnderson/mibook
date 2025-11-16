from django.urls import path

from .views import SecureRegisterView, SecureLoginView, LogoutView


urlpatterns = [
    path('login/', SecureLoginView.as_view(), name='login'),
    path('register/', SecureRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout')
]