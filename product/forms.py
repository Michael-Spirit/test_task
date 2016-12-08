from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.forms import AuthenticationForm
from .models import Comment, Product


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': "Your comment",
                'class': "form-control"})
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', )
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': "Name",
                'class': "form-control"}),
            'description': forms.Textarea(attrs={
                'placeholder': "Description",
                'class': "form-control",
                'maxlength': 140}),
            'price': forms.NumberInput(attrs={
                'placeholder': "Description",
                'class': "form-control"})
        }


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserCreationForm.Meta.model
        fields = UserCreationForm.Meta.fields
        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'placeholder': "Username"}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': "Password confirmation"}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': "Password confirmation"}),
    )


class MyAuthenticationForm(AuthenticationForm):

    username = UsernameField(
        widget=forms.TextInput(attrs={
            'autofocus': '',
            'class': "form-control",
            'placeholder': "Username"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': "form-control",
            'placeholder': "Password"})
    )
