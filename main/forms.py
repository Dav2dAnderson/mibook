from django import forms
from django.core.validators import validate_email

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label='Your Name',
        widget=forms.TextInput(attrs={
            'class': 'w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none',
            'placeholder': "Your name"
        })
    )
    email = forms.EmailField(
        label="Your Email",
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': "w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none",
            'placeholder': "your@gmail.com"
        })
    )
    message = forms.CharField(
        label="Message",
        widget=forms.Textarea(attrs={
            'class': "w-full border rounded-md px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none",
            'rows': 5,
            'placeholder': "Your message..."
        })
    )

    def clean_message(self):
        message = self.cleaned_data.get("message", "")
        if len(message.split()) < 3:
            raise forms.ValidationError("Message is too short.")
        if any(word in message.lower() for word in ["<script>", "http://", "https://"]):
            raise forms.ValidationError("Invalid content detected.")
        return message
    

