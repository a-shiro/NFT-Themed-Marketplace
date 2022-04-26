from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views
from django.core import exceptions as django_exceptions

from DesertTraders.web_generic_features.forms import CreateCollectionForm, CreateNFTForm, EditProfileForm
from DesertTraders.web_generic_features.helpers import check_if_button_active, \
    get_profile_nfts_and_nft_quantity, validate_user_info
from DesertTraders.web_generic_features.mixins import OwnerAccessMixin, CollectionAccessMixin
from DesertTraders.web_generic_features.models import Profile, Collection, NFT, Favorite
from DesertTraders.web_generic_features.views.abstract.abstract import AbstractCollectionDetailsView


class PersonalProfileWorkshopView(generic_views.DetailView, mixins.LoginRequiredMixin, OwnerAccessMixin):
    template_name = 'web_generic_features/profile/personal_profile/personal_workshop.html'
    model = Profile

    def get_context_data(self, **kwargs):
        profile_collections = Collection.objects.filter(user=self.request.user).order_by('-posted_for_sale')
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['profile_collections'] = profile_collections
        context['nft_add_button_active'] = nft_add_button_active

        return context


class PersonalProfileCollectionView(generic_views.DetailView, mixins.LoginRequiredMixin, OwnerAccessMixin):
    template_name = 'web_generic_features/profile/personal_profile/personal_collection.html'
    model = Profile

    def get_context_data(self, **kwargs):
        profile_nfts_and_nft_quantity = get_profile_nfts_and_nft_quantity(self.object)
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['profile_nfts_and_nft_quantity'] = profile_nfts_and_nft_quantity
        context['nft_add_button_active'] = nft_add_button_active

        return context


class WorkshopCollectionDetailsView(AbstractCollectionDetailsView, mixins.LoginRequiredMixin, CollectionAccessMixin):
    template_name = 'web_generic_features/profile/personal_profile/workshop_collection_details.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, pk=kwargs['pk'], posted_for_sale=False)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class PersonalProfileFavoriteView(generic_views.DetailView, OwnerAccessMixin):
    template_name = 'web_generic_features/profile/personal_profile/personal_favorite.html'
    model = Profile

    def get_context_data(self, **kwargs):
        favorite_nfts = NFT.objects.filter(favorite__profile_id=self.object, favorite__favorite=True)
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['favorite_nfts'] = favorite_nfts
        context['nft_add_button_active'] = nft_add_button_active

        return context


class EditProfileView(generic_views.UpdateView, mixins.LoginRequiredMixin, OwnerAccessMixin):
    template_name = 'web_generic_features/profile/personal_profile/edit_profile.html'
    model = Profile
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('personal profile workshop', kwargs={'pk': self.request.user.pk})


class CreateCollectionView(generic_views.CreateView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/create_collection.html'
    form_class = CreateCollectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse_lazy('personal profile workshop', kwargs={'pk': self.request.user.pk})


class CreateNFTView(generic_views.CreateView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/create_nft.html'
    form_class = CreateNFTForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse_lazy('personal profile workshop', kwargs={'pk': self.request.user.pk})


@login_required
def post_on_market(request, pk):
    try:
        collection = Collection.objects.get(pk=pk, posted_for_sale=False)

        validate_user_info(request, collection)

        collection.posted_for_sale = True

        collection.save()

        return redirect('personal profile workshop', request.user.pk)
    except django_exceptions.ObjectDoesNotExist:
        return redirect('404')

    except django_exceptions.BadRequest:
        return redirect('400')


@login_required
def remove_collection(request, pk):
    try:
        collection = Collection.objects.get(pk=pk, posted_for_sale=False)

        validate_user_info(request, collection)

        collection.delete()

        return redirect('personal profile workshop', request.user.pk)
    except django_exceptions.ObjectDoesNotExist:
        return redirect('404')

    except django_exceptions.BadRequest:
        return redirect('400')


@login_required
def remove_nft(request, pk):
    try:
        nft = NFT.objects.get(pk=pk, collection__posted_for_sale=False)
        collection = nft.collection

        validate_user_info(request, collection)

        nft.delete()

        return redirect('personal profile workshop', request.user.pk)
    except django_exceptions.ObjectDoesNotExist:
        return redirect('404')

    except django_exceptions.BadRequest:
        return redirect('400')



