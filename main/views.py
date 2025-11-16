import json

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, TemplateView, FormView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from .models import Post, Replies
from .forms import PostForm, ContactForm

import logging


logger = logging.getLogger(__name__)
# Create your views here.


class ProfileView(DetailView):
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


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'body']
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'
    # success_url = reverse_lazy('profile_user')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse('profile_user', kwargs={'username': self.request.user.username})
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def get_success_url(self):
        return reverse('feed_page')


class FeedView(ListView):
    model = Post
    template_name = 'feed.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
        
            return render(request, 'post_items.html', {'post': post})
        else:
            # Return form errors
            return HttpResponse("Invalid form data", status=400)
        

@login_required
def toggle_like(request):
    if request.method == "POST":
        slug = request.POST.get("slug")
        post = get_object_or_404(Post, slug=slug)

        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            "liked": liked,
            "total_likes": post.total_likes()
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


class PostReplyView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_reply.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        content = request.POST.get("content")
        if content:
            Replies.objects.create(
                post = self.object,
                author = self.request.user,
                body = content
            )
        return redirect('post_reply', slug=self.object.slug)
    


# Other stuff

class AboutProjectView(TemplateView):
    template_name = 'about_project.html'




class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        user_ip = self.request.META.get('REMOTE_ADDR')

        subject = f"New message from {name}"
        body = f"From: {name} <{email}>\nIP: {user_ip}\n\n{message}"

        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except BadHeaderError:
            logger.error(f"Bad header in email from {email}")
        except Exception as e:
            logger.error(f"Error sending contact form: {e}")

        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.error(f"Invalid contact form submission: {form.errors}")
        return super().form_invalid(form)
    

def test_base(request):
    return render(request, 'base.html')
