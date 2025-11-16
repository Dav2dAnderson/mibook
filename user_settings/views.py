from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import mixins, views
from django.views import View
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your views here.


class ProfileView(generic.DetailView):
    model = User
    template_name = 'profile_related/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.all()
        return context
    

class ProfileEditView(View):
    def get(self, request):
        return render(request, 'profile_related/profile_edit.html')
    
    def post(self, request):
        user = request.user
        profile = user.profile

        profile.bio = request.POST.get("bio")
        email = request.POST.get('email')
        if email and email != user.email:
            user.email = email
            user.save()

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if first_name or last_name:
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        
        if "image" in request.FILES:
            profile.image = request.FILES["image"]
        profile.save()

        return redirect("profile_user", username=user.username)
    

class UserPasswordChangeView(mixins.LoginRequiredMixin, views.PasswordChangeView):
    template_name = 'profile_related/password_change.html'
    
    def get_success_url(self):
        return reverse_lazy('profile_user', kwargs={'username': self.request.user.username})

