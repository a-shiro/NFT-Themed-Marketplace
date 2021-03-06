from django.contrib.auth import forms as dj_auth_forms
from django import forms

from DesertTraders.users.models import CustomUser
from DesertTraders.web_generic_features.models import Profile
from DesertTraders.users.validators import alphanumeric_validator


class CustomUserRegisterForm(dj_auth_forms.UserCreationForm):
    USERNAME_MAX_LENGTH_VALUE = 25

    username = forms.CharField(
        max_length=USERNAME_MAX_LENGTH_VALUE,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'e.g. George27',
            }
        ),
        validators=(alphanumeric_validator,)
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**************',
            }
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**************'
            }
        )
        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'e.g. George27',
            }
        )

    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'class': "form-control",
                    'placeholder': '...@example.com',
                }
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile = Profile(
            username=self.cleaned_data['username'],
            user=user,
        )

        if commit:
            profile.save()

        return user


class CustomUserLoginForm(dj_auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '.....'
            }
        )

        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '.....'
            }
        )
