from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic as generic_views
from django.core import exceptions as django_exceptions
from django.contrib.auth import mixins

from DesertTraders.web_generic_features.helpers import transaction, validate_info, favorite_nft, get_nfts_and_favorite
from DesertTraders.web_generic_features.models import Profile, NFT, Collection
from DesertTraders.web_generic_features.views.abstract.abstract import AbstractCollectionDetailsView


class MarketplaceView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/marketplace.html'

    def get_context_data(self, **kwargs):
        marketplace_collections = Collection.objects.filter(posted_for_sale=True)
        marketplace_collections_count = len(marketplace_collections)

        context = super().get_context_data(**kwargs)

        context['marketplace_collections'] = marketplace_collections
        context['marketplace_collections_count'] = marketplace_collections_count
        return context


class CollectionDetailsView(AbstractCollectionDetailsView):
    template_name = 'web_generic_features/marketplace/collection_details.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, pk=kwargs['pk'], posted_for_sale=True)

    def get_context_data(self, **kwargs):
        nfts_and_favorite_pair = get_nfts_and_favorite(pk=self.object.pk, profile=self.request.user.profile)

        context = super().get_context_data(**kwargs)
        context['nfts_and_favorite_pair'] = nfts_and_favorite_pair

        return context


@login_required
def buy_nft(request, pk):
    profile = Profile.objects.get(user=request.user)

    try:
        nft = NFT.objects.get(pk=pk, collection__posted_for_sale=True)

        if validate_info(profile, nft):
            return redirect('400')

        transaction(profile, nft)

        return redirect('collection details', nft.collection.pk)
    except django_exceptions.ObjectDoesNotExist:
        return redirect('404')


class FavoriteNFTView(generic_views.View, mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                favorite_nft(request.user.profile, kwargs['pk'])

                return self.redirect(**kwargs)
            except django_exceptions.ObjectDoesNotExist:
                return redirect('404')

    @staticmethod
    def redirect(**kwargs):
        collection = NFT.objects.get(pk=kwargs['pk']).collection

        return redirect('collection details', collection.pk)


class SortCollectionView(CollectionDetailsView):
    def get_context_data(self, **kwargs):
        nfts_and_favorite_pair = get_nfts_and_favorite(pk=self.object.pk, profile=self.request.user.profile, ordering=self.request.GET['sort'])

        context = super().get_context_data(**kwargs)
        context['nfts_and_favorite_pair'] = nfts_and_favorite_pair

        return context
