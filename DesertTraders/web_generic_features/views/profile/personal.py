from django.contrib.auth import mixins
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as dj_generic
from django.core import exceptions as django_exceptions

from DesertTraders.web_generic_features.forms import CreateCollectionForm, CreateNFTForm, EditProfileForm
from DesertTraders.web_generic_features.views.profile.public import PublicProfileWorkshopView
from DesertTraders.web_generic_features.views.view_helpers.helpers import check_if_button_active, \
    get_profile_nfts_and_nft_quantity, validate_user_info
from DesertTraders.web_generic_features.views.view_helpers.mixins import CollectionAccessMixin
from DesertTraders.web_generic_features.models import Profile, Collection, NFT
from DesertTraders.web_generic_features.views.view_helpers.abstract import AbstractCollectionDetailsView


class ProfileView(dj_generic.View):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.pk != kwargs['pk']:
            return PublicProfileWorkshopView.as_view()(self.request, pk=kwargs['pk'])
        return PersonalProfileWorkshopView.as_view()(self.request, pk=kwargs['pk'])


class PersonalProfileWorkshopView(dj_generic.DetailView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/personal_workshop.html'
    model = Profile

    def get_context_data(self, **kwargs):
        profile_collections = Collection.objects.filter(user=self.request.user).order_by('-posted_for_sale')
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['profile_collections'] = profile_collections
        context['nft_add_button_active'] = nft_add_button_active

        return context


class PersonalProfileCollectionView(dj_generic.DetailView, mixins.LoginRequiredMixin):
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


class PersonalProfileFavoriteView(dj_generic.DetailView):
    template_name = 'web_generic_features/profile/personal_profile/personal_favorite.html'
    model = Profile

    def get_context_data(self, **kwargs):
        favorite_nfts = NFT.objects.filter(favorite__profile_id=self.object, favorite__favorite=True)
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['favorite_nfts'] = favorite_nfts
        context['nft_add_button_active'] = nft_add_button_active

        return context


class EditProfileView(dj_generic.UpdateView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/edit_profile.html'
    model = Profile
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('personal profile workshop', kwargs={'pk': self.request.user.pk})


class CreateCollectionView(dj_generic.CreateView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/create_collection.html'
    form_class = CreateCollectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse_lazy('personal profile workshop', kwargs={'pk': self.request.user.pk})


class CreateNFTView(dj_generic.CreateView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/create_nft.html'
    form_class = CreateNFTForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse_lazy('personal profile workshop', kwargs={'pk': self.request.user.pk})


class PostOnMarketView(dj_generic.View, mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            collection = Collection.objects.get(pk=kwargs['pk'], posted_for_sale=False)

            validate_user_info(request, collection)

            collection.posted_for_sale = True

            collection.save()

            return self.redirect()
        except django_exceptions.ObjectDoesNotExist:
            return redirect('404')

        except django_exceptions.BadRequest:
            return redirect('400')

    def redirect(self):
        return redirect('personal profile workshop', self.request.user.pk)


class RemoveCollectionView(dj_generic.View, mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            collection = Collection.objects.get(pk=kwargs['pk'], posted_for_sale=False)

            validate_user_info(request, collection)

            collection.delete()

            return self.redirect()
        except django_exceptions.ObjectDoesNotExist:
            return redirect('404')

        except django_exceptions.BadRequest:
            return redirect('400')

    def redirect(self):
        return redirect('personal profile workshop', self.request.user.pk)


class RemoveNFTView(dj_generic.View, mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        try:
            nft = NFT.objects.get(pk=kwargs['pk'], collection__posted_for_sale=False)
            collection = nft.collection

            validate_user_info(request, collection)

            nft.delete()

            return self.redirect()
        except django_exceptions.ObjectDoesNotExist:
            return redirect('404')

        except django_exceptions.BadRequest:
            return redirect('400')

    def redirect(self):
        return redirect('personal profile workshop', self.request.user.pk)  # Fix to redirect to collection
