from django import forms

from DesertTraders.web_generic_features.models import Collection, NFT


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


class CreateNFTForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(CreateNFTForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['collection'].queryset = Collection.objects.filter(user=user)

    class Meta:
        model = NFT
        fields = '__all__'
