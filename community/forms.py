from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'content',
        ]
        widgets = {
            'title': forms.Textarea(attrs={"rows": 1})
        }

class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='',)
    class Meta:
        model = Comment
        fields = [
            'comment',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={"rows": 2}, )
        }
