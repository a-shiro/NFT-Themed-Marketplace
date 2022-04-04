from django.contrib.auth import forms as auth_forms
from django import forms as input_forms

from DesertTraders.users.models import CustomUser
from DesertTraders.web_generic_features.models import Profile


class CustomUserRegisterForm(auth_forms.UserCreationForm):
    username = input_forms.CharField(max_length=25)

    def __init__(self, *args, **kwargs):
        super(CustomUserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = input_forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**************',
            }
        )
        self.fields['password2'].widget = input_forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '**************'
            }
        )
        self.fields['username'].widget = input_forms.TextInput(
            attrs={
                'class': "form-control",
                'placeholder': 'e.g. George27',
            }
        )

    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {
            'email': input_forms.EmailInput(
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


class CustomUserLoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = input_forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '.....'
            }
        )

        self.fields['password'].widget = input_forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '.....'
            }
        )
