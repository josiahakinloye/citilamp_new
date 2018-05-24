from django import forms


class PostCommentForm(forms.Form):
    comment = forms.CharField(max_length=255)
