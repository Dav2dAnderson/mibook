from django.urls import path

from .views import UserPasswordChangeView, ProfileEditView, ProfileView


urlpatterns = [
    path('change-password/', UserPasswordChangeView.as_view(), name='change_password'),
    path('profile_edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('u/<slug:username>/', ProfileView.as_view(), name='profile_user'),
]