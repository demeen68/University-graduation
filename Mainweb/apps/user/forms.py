from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class ResetPasswordForm(forms.Form):
    password1 = forms.CharField(required=True, max_length=50)
    password2 = forms.CharField(required=True, max_length=50)


class AddUserForm(forms.Form):
    username = forms.CharField(required=True, max_length=255)
    password1 = forms.CharField(required=True, max_length=50)
    password2 = forms.CharField(required=True, max_length=50)
