# Django
from django import forms
from comment.models import Comment

"""Esta es otra forma de crear Formularios (ModelForm)"""
class CommentForm(forms.ModelForm):
    """Comment model form."""
    body = forms.CharField(widget=forms.TextInput(attrs={
                           'class': 'input', 'placeholder': 'Enter Comment', 'style': 'width: 18.5vw;'}), required=True)

    class Meta:
        """Form settings"""
        model = Comment  # Modelo utilziar
        fields = ('body',)
