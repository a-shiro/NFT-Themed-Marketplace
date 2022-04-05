from django.contrib.auth import mixins
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic as generic_views

from DesertTraders.web_generic_features.forms import CreateCollectionForm, CreateNFTForm
from DesertTraders.web_generic_features.helpers import get_tuple_my_nfts_with_nft_quantity
from DesertTraders.web_generic_features.models import Collection, Profile


class ProfileWorkshopView(mixins.LoginRequiredMixin, generic_views.DetailView):
    template_name = 'web_generic_features/profile/workshop.html'
    model = Profile

    def get_context_data(self, **kwargs):
        user = self.object.user
        collections = Collection.objects.filter(user=user)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        context['hide_footer'] = True
        return context


class MyCollectionView(mixins.LoginRequiredMixin, generic_views.DetailView):
    template_name = 'web_generic_features/profile/my_collection.html'
    model = Profile

    def get_context_data(self, **kwargs):
        user = self.request.user
        collections = Collection.objects.filter(user=user)
        my_nfts_and_nft_quantity_pair = get_tuple_my_nfts_with_nft_quantity(self.object)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        context['my_nfts_and_nft_quantity_pair'] = my_nfts_and_nft_quantity_pair
        context['hide_footer'] = True
        return context


class CreateCollectionView(mixins.LoginRequiredMixin, generic_views.CreateView):
    template_name = 'web_generic_features/profile/create_collection.html'
    form_class = CreateCollectionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile workshop', kwargs={'pk': self.request.user.id})


class CreateNFTView(mixins.LoginRequiredMixin, generic_views.CreateView):
    template_name = 'web_generic_features/profile/create_nft.html'
    form_class = CreateNFTForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile workshop', kwargs={'pk': self.request.user.id})


@login_required
def mint_collection(request, pk):
    collection = Collection.objects.filter(pk=pk)[0]
    collection.posted_for_sale = True
    collection.save()

    return redirect('profile workshop', request.user.pk)
