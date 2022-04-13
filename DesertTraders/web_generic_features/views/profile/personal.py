from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from DesertTraders.web_generic_features.forms import CreateCollectionForm, CreateNFTForm, EditProfileForm
from DesertTraders.web_generic_features.helpers import get_profile_collections, check_if_button_active, \
    get_profile_nfts_and_nft_quantity, get_collection_with_pk, get_nft_with_pk
from DesertTraders.web_generic_features.models import Profile
from DesertTraders.web_generic_features.views.abstract import AbstractCollectionDetailsView


class PersonalProfileWorkshopView(generic_views.DetailView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/personal_workshop.html'
    model = Profile

    def get_context_data(self, **kwargs):
        collections = get_profile_collections(self.request.user)
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        context['nft_add_button_active'] = nft_add_button_active

        return context


class PersonalProfileCollectionView(generic_views.DetailView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/personal_collection.html'
    model = Profile

    def get_context_data(self, **kwargs):
        profile_nfts_and_nft_quantity = get_profile_nfts_and_nft_quantity(self.object)
        nft_add_button_active = check_if_button_active(self.request.user)

        context = super().get_context_data(**kwargs)

        context['profile_nfts_and_nft_quantity'] = profile_nfts_and_nft_quantity
        context['nft_add_button_active'] = nft_add_button_active

        return context


class WorkshopCollectionDetailsView(AbstractCollectionDetailsView, mixins.LoginRequiredMixin):
    template_name = 'web_generic_features/profile/personal_profile/workshop_collection_details.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, pk=kwargs['pk'], posted_for_sale=False)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class EditProfileView(generic_views.UpdateView, mixins.LoginRequiredMixin):
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
    collection = get_collection_with_pk(pk=pk)
    collection.posted_for_sale = True

    collection.save()

    return redirect('personal profile workshop', request.user.pk)


@login_required
def remove_collection(request, pk):
    collection = get_collection_with_pk(pk=pk)
    collection.delete()

    # implement logic that removes collection image and the nft images when collection is deleted

    return redirect('personal profile workshop', request.user.pk)


@login_required
def remove_nft(request, pk):
    nft = get_nft_with_pk(pk=pk)
    nft.delete()

    # implement logic that removes nft image from collection when is deleted

    return redirect('personal profile workshop', request.user.pk)

