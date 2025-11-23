from django.urls import path

from .views import (PostDetailView, PostUpdateView, PostDeleteView, SendMessage,
                    FeedView, PostReplyView, toggle_like, AboutProjectView, ContactView, ChatView)


urlpatterns = [
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path("post_reply/<slug:slug>/", PostReplyView.as_view(), name='post_reply'),
    path('about_project/', AboutProjectView.as_view(), name='about_project'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('chats/', ChatView.as_view(), name='chats'),
    path('chats/send/', SendMessage.as_view(), name='send_message'),
    path('toggle_like/', toggle_like, name='toggle_like'),
    path('', FeedView.as_view(), name='feed_page')
]