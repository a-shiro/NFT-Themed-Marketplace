from django.contrib.auth import mixins as dj_mixins
from django.views import generic as dj_generic
from django.core import exceptions as dj_exceptions
from django import http as dj_http
from django.urls import reverse_lazy
from django.shortcuts import redirect

from DesertTraders.web_generic_features.models import Profile, Collection, NFT
from DesertTraders.web_generic_features.forms import EditProfileForm, CreateCollectionForm, CreateNFTForm
from DesertTraders.web_generic_features.views.helpers import check_if_button_active, validate_user_info, \
    get_nfts_and_quantity
from DesertTraders.web_generic_features.views.mixins import OwnerAccessMixin, CollectionContentMixin, \
    CreateViewMixin, ActionMixin


class PersonalProfileWorkshopView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/personal/personal_workshop.html'

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(user=self.object.user).order_by('-posted_for_sale')
        add_nft = check_if_button_active(self.object.user)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        context['add_nft'] = add_nft

        return context


class PersonalProfileCollectionView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/personal/personal_collection.html'

    def get_context_data(self, **kwargs):
        nft_and_quantity_pair = get_nfts_and_quantity(self.object)
        add_nft = check_if_button_active(self.object.user)

        context = super().get_context_data(**kwargs)

        context['nft_and_quantity_pair'] = nft_and_quantity_pair
        context['add_nft'] = add_nft
        return context


class PersonalProfileFavoriteView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/personal/personal_favorite.html'

    def get_context_data(self, **kwargs):
        favorite_nfts = NFT.objects.filter(favorite__profile_id=self.object, favorite__favorite=True)
        add_nft = check_if_button_active(self.object.user)

        context = super().get_context_data(**kwargs)

        context['favorite_nfts'] = favorite_nfts
        context['add_nft'] = add_nft

        return context


class PersonalProfileCollectionDetailsView(OwnerAccessMixin, CollectionContentMixin):
    template_name = 'web_generic_features/profile/personal/workshop_collection_details.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, pk=kwargs['pk'], posted_for_sale=False)

    def get_requested_user_pk(self, **kwargs):
        requested_user_pk = Collection.objects.get(pk=kwargs['pk']).user.pk

        return requested_user_pk


class CreateCollectionView(CreateViewMixin):
    form_class = CreateCollectionForm
    template_name = 'web_generic_features/profile/personal/create_collection.html'


class CreateNFTView(CreateViewMixin):
    form_class = CreateNFTForm
    template_name = 'web_generic_features/profile/personal/create_nft.html'


class EditProfileView(dj_mixins.LoginRequiredMixin, OwnerAccessMixin, dj_generic.UpdateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'web_generic_features/profile/personal/edit_profile.html'

    def get_context_data(self, **kwargs):
        add_nft = check_if_button_active(self.object.user)

        context = super().get_context_data(**kwargs)

        context['add_nft'] = add_nft
        return context

    def get_success_url(self):
        profile_pk = self.object.pk

        return reverse_lazy('profile', kwargs={'pk': profile_pk})


class SellOnMarketView(dj_mixins.LoginRequiredMixin, ActionMixin):
    REDIRECT_TO = 'profile'

    def action(self, request, collection):
        owner_pk = collection.user.pk

        validate_user_info(request, owner_pk)

        collection.posted_for_sale = True
        collection.save()

        return None

    def get_instance(self, **kwargs):
        try:
            collection_pk = kwargs['pk']

            instance = Collection.objects.get(pk=collection_pk, posted_for_sale=False)

            return instance
        except dj_exceptions.ObjectDoesNotExist:
            raise dj_http.Http404

    def redirect(self, *args, **kwargs):
        redirect_to = self.REDIRECT_TO
        redirect_pk = self.request.user.pk

        return redirect(redirect_to, redirect_pk)


class RemoveCollectionView(dj_mixins.LoginRequiredMixin, ActionMixin):
    REDIRECT_TO = 'profile'

    def action(self, request, collection):
        owner_pk = collection.user.pk

        validate_user_info(request, owner_pk)

        collection.delete()

        return None

    def get_instance(self, **kwargs):
        try:
            collection_pk = kwargs['pk']

            instance = Collection.objects.get(pk=collection_pk, posted_for_sale=False)

            return instance
        except dj_exceptions.ObjectDoesNotExist:
            raise dj_http.Http404

    def redirect(self, *args, **kwargs):
        redirect_to = self.REDIRECT_TO
        redirect_pk = self.request.user.pk

        return redirect(redirect_to, redirect_pk)


class RemoveNFTView(dj_mixins.LoginRequiredMixin, ActionMixin):
    REDIRECT_TO = 'personal collection details'
    redirect_pk = None

    def action(self, request, nft):
        owner_pk = nft.collection.user.pk

        validate_user_info(request, owner_pk)

        nft.delete()

        return None

    def get_instance(self, **kwargs):
        try:
            nft_pk = self.kwargs['pk']
            self.redirect_pk = NFT.objects.get(pk=nft_pk).collection.pk

            instance = NFT.objects.get(pk=nft_pk, collection__posted_for_sale=False)

            return instance
        except dj_exceptions.ObjectDoesNotExist:
            raise dj_http.Http404

    def redirect(self, *args, **kwargs):
        redirect_to = self.REDIRECT_TO
        redirect_pk = self.redirect_pk

        return redirect(redirect_to, redirect_pk)
