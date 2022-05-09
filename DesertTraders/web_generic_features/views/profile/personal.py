from django.contrib.auth import mixins as dj_mixins
from django.views import generic as dj_generic
from django.urls import reverse_lazy

from DesertTraders.web_generic_features.models import Profile, Collection, NFT
from DesertTraders.web_generic_features.forms import EditProfileForm, CreateCollectionForm, CreateNFTForm
from DesertTraders.web_generic_features.views.view_helpers.helpers import check_if_button_active, \
    get_profile_nfts_and_nft_quantity, validate_and_sell, validate_and_remove
from DesertTraders.web_generic_features.views.view_helpers.mixins import OwnerAccessMixin, CollectionContentMixin, \
    CreateViewMixin, ActionMixin


class PersonalProfileWorkshopView(dj_generic.DetailView, dj_mixins.LoginRequiredMixin):
    model = Profile
    template_name = 'web_generic_features/profile/personal_profile/personal_workshop.html'

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(user=self.object.user).order_by('-posted_for_sale')
        add_nft = check_if_button_active(self.object.user)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        context['add_nft'] = add_nft

        return context


class PersonalProfileCollectionView(dj_generic.DetailView, dj_mixins.LoginRequiredMixin):
    model = Profile
    template_name = 'web_generic_features/profile/personal_profile/personal_collection.html'

    def get_context_data(self, **kwargs):
        nft_and_quantity_pair = get_profile_nfts_and_nft_quantity(self.object)
        add_nft = check_if_button_active(self.object.user)

        context = super().get_context_data(**kwargs)

        context['nft_and_quantity_pair'] = nft_and_quantity_pair
        context['add_nft'] = add_nft
        return context


class PersonalProfileFavoriteView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/personal_profile/personal_favorite.html'

    def get_context_data(self, **kwargs):
        favorite_nfts = NFT.objects.filter(favorite__profile_id=self.object, favorite__favorite=True)
        add_nft = check_if_button_active(self.object.user)

        context = super().get_context_data(**kwargs)

        context['favorite_nfts'] = favorite_nfts
        context['add_nft'] = add_nft

        return context


class PersonalProfileCollectionDetailsView(dj_mixins.LoginRequiredMixin, CollectionContentMixin, OwnerAccessMixin):
    template_name = 'web_generic_features/profile/personal_profile/workshop_collection_details.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, pk=kwargs['pk'], posted_for_sale=False)


class CreateCollectionView(CreateViewMixin):
    form_class = CreateCollectionForm
    template_name = 'web_generic_features/profile/personal_profile/create_collection.html'


class CreateNFTView(CreateViewMixin):
    form_class = CreateNFTForm
    template_name = 'web_generic_features/profile/personal_profile/create_nft.html'


class EditProfileView(dj_generic.UpdateView, dj_mixins.LoginRequiredMixin):
    model = Profile
    form_class = EditProfileForm
    template_name = 'web_generic_features/profile/personal_profile/edit_profile.html'

    def get_success_url(self):
        profile_pk = self.object.pk

        return reverse_lazy('profile', kwargs={'pk': profile_pk})


class SellOnMarketView(ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        collection = Collection.objects.get(pk=kwargs['pk'], posted_for_sale=False)

        super().dispatch(request, instance=collection, action=validate_and_sell)

        return self.redirect(*args, **kwargs)

    def redirect(self, *args, **kwargs):
        profile_pk = self.request.user.pk

        return super().redirect(redirect_to='profile', redirect_pk=profile_pk)


class RemoveCollectionView(ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        collection = Collection.objects.get(pk=kwargs['pk'], posted_for_sale=False)

        super().dispatch(request, instance=collection, action=validate_and_remove)

        return self.redirect(*args, **kwargs)

    def redirect(self, *args, **kwargs):
        profile_pk = self.request.user.pk

        return super().redirect(redirect_to='profile', redirect_pk=profile_pk)


class RemoveNFTView(ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        nft = NFT.objects.get(pk=kwargs['pk'], collection__posted_for_sale=False)
        collection_pk = nft.collection.pk

        super().dispatch(request, instance=nft, action=validate_and_remove)

        return self.redirect(collection_pk=collection_pk)

    def redirect(self, *args, **kwargs):
        collection_pk = kwargs['collection_pk']

        return super().redirect(redirect_to='personal collection details', redirect_pk=collection_pk)
