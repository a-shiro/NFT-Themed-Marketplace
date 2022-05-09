from django.contrib.auth import mixins as dj_mixins
from django.views import generic as generic_views

from DesertTraders.web_generic_features.models import NFT, Collection, Favorite
from DesertTraders.web_generic_features.views.view_helpers.helpers import transaction, favorite_nft, \
    get_nfts_and_favorite, get_nfts_when_user_anonymous
from DesertTraders.web_generic_features.views.view_helpers.mixins import CollectionContentMixin, ActionMixin


class MarketplaceView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/marketplace.html'

    def get_context_data(self, **kwargs):
        marketplace_collections = Collection.objects.filter(posted_for_sale=True)
        marketplace_collections_count = len(marketplace_collections)

        context = super().get_context_data(**kwargs)

        context['marketplace_collections'] = marketplace_collections
        context['marketplace_collections_count'] = marketplace_collections_count
        return context


class CollectionDetailsView(CollectionContentMixin):
    template_name = 'web_generic_features/marketplace/collection_details.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, pk=kwargs['pk'], posted_for_sale=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        nfts = context['total_nfts']

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            nfts_and_favorite_pair = get_nfts_and_favorite(iterable=nfts, profile=profile)
        else:
            nfts_and_favorite_pair = get_nfts_when_user_anonymous(iterable=nfts)

        context['nfts_and_favorite_pair'] = nfts_and_favorite_pair

        return context


class SortCollectionView(CollectionDetailsView):
    def get_context_data(self, **kwargs):
        nfts = self.object.nft_set.all()
        ordering = self.request.GET['sort']

        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            nfts_and_favorite_pair = get_nfts_and_favorite(iterable=nfts, profile=profile, ordering=ordering)
        else:
            nfts_and_favorite_pair = get_nfts_when_user_anonymous(iterable=nfts, ordering=ordering)

        context['nfts_and_favorite_pair'] = nfts_and_favorite_pair

        return context


class SearchMarketplaceView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/marketplace_search.html'

    def get_context_data(self, **kwargs):
        searched = self.request.GET['searched']

        searched_results = NFT.objects.filter(title__contains=searched, collection__posted_for_sale=True)
        searched_results_count = len(searched_results)

        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            nfts_and_favorite_pair = get_nfts_and_favorite(iterable=searched_results, profile=profile)
        else:
            nfts_and_favorite_pair = get_nfts_when_user_anonymous(iterable=searched_results)

        context['nfts_and_favorite_pair'] = nfts_and_favorite_pair
        context['searched_results_count'] = searched_results_count

        return context


class BuyNFTView(dj_mixins.LoginRequiredMixin, ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            nft = NFT.objects.get(pk=kwargs['pk'])

            super().dispatch(request, instance=nft, action=transaction)

            return self.redirect(nft_pk=nft.pk)
        return super().dispatch(request, *args, **kwargs)

    def redirect(self, *args, **kwargs):
        collection_pk = NFT.objects.get(pk=kwargs['nft_pk']).collection.pk

        return super().redirect(redirect_to='collection details', redirect_pk=collection_pk)


class FavoriteNFTView(dj_mixins.LoginRequiredMixin, ActionMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            nft = NFT.objects.get(pk=kwargs['pk'])
            profile = self.request.user.profile

            favorite = Favorite.objects.get(nft=nft, profile=profile)

            super().dispatch(request, instance=favorite, action=favorite_nft)

            return self.redirect(nft_pk=nft.pk)
        return super().dispatch(request, *args, **kwargs)

    def redirect(self, *args, **kwargs):
        collection_pk = NFT.objects.get(pk=kwargs['nft_pk']).collection.pk

        return super().redirect(redirect_to='collection details', redirect_pk=collection_pk)
