from django.contrib.auth import mixins as dj_mixins
from django.views import generic as dj_generic
from django.core import exceptions as dj_exceptions
from django.shortcuts import redirect
from django.urls import reverse_lazy

from DesertTraders.web_generic_features.forms import EditProfileForm, CreateCollectionForm, CreateNFTForm
from DesertTraders.web_generic_features.models import Profile, Collection, NFT
from DesertTraders.web_generic_features.views.view_helpers.helpers import check_if_button_active, \
    get_profile_nfts_and_nft_quantity, validate_user_info, validate_and_post, validate_and_remove
from DesertTraders.web_generic_features.views.view_helpers.mixins import OwnerAccessMixin, CollectionContentMixin, \
    CreateViewMixin, ActionMixin


class PersonalProfileWorkshopView(dj_generic.DetailView, dj_mixins.LoginRequiredMixin):
    model = Profile
    template_name = 'web_generic_features/profile/personal_profile/personal_workshop.html'

    def get_context_data(self, **kwargs):
        profile_collections = Collection.objects.filter(user=self.request.user).order_by('-posted_for_sale')
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['profile_collections'] = profile_collections
        context['nft_add_button_active'] = nft_add_button_active

        return context


class PersonalProfileCollectionView(dj_generic.DetailView, dj_mixins.LoginRequiredMixin):
    model = Profile
    template_name = 'web_generic_features/profile/personal_profile/personal_collection.html'

    def get_context_data(self, **kwargs):
        profile_nfts_and_nft_quantity = get_profile_nfts_and_nft_quantity(self.object)
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['profile_nfts_and_nft_quantity'] = profile_nfts_and_nft_quantity
        context['nft_add_button_active'] = nft_add_button_active
        return context


class PersonalProfileFavoriteView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/personal_profile/personal_favorite.html'

    def get_context_data(self, **kwargs):
        favorite_nfts = NFT.objects.filter(favorite__profile_id=self.object, favorite__favorite=True)
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['favorite_nfts'] = favorite_nfts
        context['nft_add_button_active'] = nft_add_button_active

        return context


class WorkshopCollectionDetailsView(dj_mixins.LoginRequiredMixin, CollectionContentMixin, OwnerAccessMixin):
    template_name = 'web_generic_features/profile/personal_profile/workshop_collection_details.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, pk=kwargs['pk'], posted_for_sale=False)


class EditProfileView(dj_generic.UpdateView, dj_mixins.LoginRequiredMixin):
    model = Profile
    form_class = EditProfileForm
    template_name = 'web_generic_features/profile/personal_profile/edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})


class CreateCollectionView(CreateViewMixin):
    form_class = CreateCollectionForm
    template_name = 'web_generic_features/profile/personal_profile/create_collection.html'


class CreateNFTView(CreateViewMixin):
    form_class = CreateNFTForm
    template_name = 'web_generic_features/profile/personal_profile/create_nft.html'


class PostOnMarketView(ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            collection = Collection.objects.get(pk=kwargs['pk'], posted_for_sale=False)

            super().dispatch(request, instance=collection, action=validate_and_post)

            return self.redirect()

        except dj_exceptions.ObjectDoesNotExist:
            return redirect('404')
        except dj_exceptions.BadRequest:
            return redirect('400')


class RemoveCollectionView(ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            collection = Collection.objects.get(pk=kwargs['pk'], posted_for_sale=False)

            super().dispatch(request, instance=collection, action=validate_and_remove)

            return self.redirect()

        except dj_exceptions.ObjectDoesNotExist:
            return redirect('404')
        except dj_exceptions.BadRequest:
            return redirect('400')


class RemoveNFTView(ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            nft = NFT.objects.get(pk=kwargs['pk'], collection__posted_for_sale=False)
            redirect_to = nft.collection.pk

            super().dispatch(request, instance=nft, action=validate_and_remove)

            return self.redirect(redirect_to)

        except dj_exceptions.ObjectDoesNotExist:
            return redirect('404')
        except dj_exceptions.BadRequest:
            return redirect('400')

    def redirect(self, redirect_to):
        return redirect('workshop collection', redirect_to)

