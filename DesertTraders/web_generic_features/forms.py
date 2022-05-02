from django import forms

from DesertTraders.web_generic_features.models import Collection, NFT, Profile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('username', 'profile_image', 'cover_image')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': "form-control",
                }
            ),
            'profile_image': forms.FileInput(
                attrs={
                    'class': "form-control",
                }
            ),
            'cover_image': forms.FileInput(
                attrs={
                    'class': "form-control",
                }
            ),
        }


class CreateCollectionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        collection = super().save(commit=False)

        collection.user = self.user
        if commit:
            collection.save()

        return collection

    class Meta:
        model = Collection
        exclude = ('user', 'posted_for_sale')
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': 'Give your collection a title...'
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': "form-control",
                }
            ),
            'cover_image': forms.FileInput(
                attrs={
                    'class': "form-control",
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': "form-control",
                    'rows': 5,
                    'placeholder': "Add a customized description...",
                }
            ),
        }


class CreateNFTForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CreateNFTForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['collection'].queryset = Collection.objects.filter(user=user, posted_for_sale=False)

    class Meta:
        model = NFT
        exclude = ('likes',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': "form-control",
                }
            ),
            'image': forms.FileInput(
                attrs={
                    'class': "form-control",
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': "form-control"
                }
            ),
            'blockchain': forms.Select(
                attrs={
                    'class': "form-control"
                }
            ),
            'collection': forms.Select(
                attrs={
                    'class': "form-control"
                }
            ),
        }
