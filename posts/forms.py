"""Post forms."""
# Django
from django import forms

# Models
from posts.models import Post

"""Esta es otra forma de crear modelos (ModelForm)"""


class PostForm(forms.ModelForm):
    """Post model form."""
    class Meta:
        """Form settings"""
        model = Post
        fields = ('user', 'profile', 'title', 'photo')
