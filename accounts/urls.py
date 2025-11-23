from django.urls import path

from .views import SecureRegisterView, SecureLoginView, LogoutView, follow_toggle


urlpatterns = [
    path('login/', SecureLoginView.as_view(), name='login'),
    path('register/', SecureRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('follow/<str:username>/', follow_toggle, name='follow_toggle')
]