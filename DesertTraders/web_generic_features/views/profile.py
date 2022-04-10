from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from DesertTraders.web_generic_features.forms import CreateCollectionForm, CreateNFTForm, EditProfileForm
from DesertTraders.web_generic_features.helpers import get_tuple_my_nfts_with_nft_quantity, check_if_button_active
from DesertTraders.web_generic_features.models import Collection, Profile


class PersonalProfileView(mixins.LoginRequiredMixin, generic_views.DetailView):
    template_name = 'web_generic_features/profile/personal_profile/personal_workshop.html'
    model = Profile

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(user=self.object.user).order_by('-posted_for_sale')
        add_nft_button_active = check_if_button_active(collections)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        context['add_nft_button_active'] = add_nft_button_active
        return context


class PersonalCollectionView(mixins.LoginRequiredMixin, generic_views.DetailView):
    template_name = 'web_generic_features/profile/personal_profile/personal_collection.html'
    model = Profile

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(user=self.object.user)
        my_nfts_and_nft_quantity_pair = get_tuple_my_nfts_with_nft_quantity(self.object)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        context['my_nfts_and_nft_quantity_pair'] = my_nfts_and_nft_quantity_pair
        return context


class EditProfileView(generic_views.UpdateView):
    template_name = 'web_generic_features/profile/personal_profile/edit_profile.html'
    model = Profile
    form_class = EditProfileForm

    def get_success_url(self):
        return reverse_lazy('personal profile', kwargs={'pk': self.request.user.pk})


class CreateCollectionView(mixins.LoginRequiredMixin, generic_views.CreateView):
    template_name = 'web_generic_features/profile/personal_profile/create_collection.html'
    form_class = CreateCollectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('personal profile', kwargs={'pk': self.request.user.pk})


class CreateNFTView(mixins.LoginRequiredMixin, generic_views.CreateView):
    template_name = 'web_generic_features/profile/personal_profile/create_nft.html'
    form_class = CreateNFTForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('personal profile', kwargs={'pk': self.request.user.pk})


@login_required
def mint_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    collection.posted_for_sale = True
    collection.save()

    return redirect('personal profile', request.user.pk)


@login_required
def remove_collection(request, pk):
    collection = Collection.objects.get(pk=pk)
    collection.delete()

    # implement logic that removes collection image and the nft images when collection is deleted

    return redirect('personal profile', request.user.pk)


class PublicProfileView(generic_views.DetailView):
    template_name = 'web_generic_features/profile/public_profile/public_workshop.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            current_session_user = int(self.request.session.get('_auth_user_id'))
            if current_session_user == self.kwargs['pk']:
                return redirect('personal profile', pk=self.kwargs['pk'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(user=self.object.user, posted_for_sale=True)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        return context


class PublicProfileCollectionView(generic_views.DetailView):
    template_name = 'web_generic_features/profile/public_profile/public_collection.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            current_session_user = int(self.request.session.get('_auth_user_id'))
            if current_session_user == self.kwargs['pk']:
                return redirect('personal collection', pk=self.kwargs['pk'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(user=self.object.user, posted_for_sale=True)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        return context
