from django.contrib.auth import mixins as dj_mixins
from django.core import exceptions as dj_exceptions
from django import http as dj_http
from django.utils import datastructures as dj_datastructures
from django.views import generic as dj_generic
from django.shortcuts import redirect

from DesertTraders.web_generic_features.models import NFT, Collection, Favorite, Collected
from DesertTraders.web_generic_features.views.helpers import get_nfts_and_favorite, \
    get_nfts_when_user_anonymous
from DesertTraders.web_generic_features.views.mixins import CollectionContentMixin, ActionMixin


class MarketplaceView(dj_generic.TemplateView):
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

        try:
            ordering = self.request.GET['sort']
        except dj_datastructures.MultiValueDictKeyError:
            ordering = 'title'

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            nfts_and_favorite_pair = get_nfts_and_favorite(iterable=nfts, profile=profile, ordering=ordering)
        else:
            nfts_and_favorite_pair = get_nfts_when_user_anonymous(iterable=nfts, ordering=ordering)

        context = super().get_context_data(**kwargs)

        context['nfts_and_favorite_pair'] = nfts_and_favorite_pair

        return context


class SearchMarketplaceView(dj_generic.TemplateView):
    template_name = 'web_generic_features/marketplace/marketplace_search.html'

    def get_context_data(self, **kwargs):
        try:
            searched = self.request.GET['searched']
        except dj_datastructures.MultiValueDictKeyError:
            raise dj_http.Http404

        searched_results = NFT.objects.filter(title__contains=searched, collection__posted_for_sale=True)
        searched_results_count = len(searched_results)

        if self.request.user.is_authenticated:
            profile = self.request.user.profile

            nfts_and_favorite_pair = get_nfts_and_favorite(iterable=searched_results, profile=profile)
        else:
            nfts_and_favorite_pair = get_nfts_when_user_anonymous(iterable=searched_results)

        context = super().get_context_data(**kwargs)

        context['nfts_and_favorite_pair'] = nfts_and_favorite_pair
        context['searched_results_count'] = searched_results_count

        return context


class BuyNFTView(dj_mixins.LoginRequiredMixin, ActionMixin):
    REDIRECT_TO = 'collection details'

    def action(self, request, nft):
        profile = request.user.profile

        if nft.pk in profile.collected_set.values_list('NFT', flat=True):
            collected_nft = profile.collected_set.get(NFT=nft)
            collected_nft.quantity += 1
            collected_nft.save()
        else:
            profile_collection = Collected(profile=profile, NFT=nft, quantity=1)
            profile_collection.save()

        profile.balance -= nft.price
        nft.quantity -= 1

        profile.save()
        nft.save()

        return None

    def get_instance(self, **kwargs):
        try:
            profile_balance = self.request.user.profile.balance
            nft_pk = kwargs['pk']

            instance = NFT.objects.get(pk=nft_pk, collection__posted_for_sale=True)

            if profile_balance < instance.price:
                raise dj_exceptions.BadRequest

            return instance
        except dj_exceptions.ObjectDoesNotExist:
            raise dj_http.Http404

    def redirect(self, *args, **kwargs):
        nft_pk = self.kwargs['pk']
        collection_pk = NFT.objects.get(pk=nft_pk).collection.pk

        redirect_to = self.REDIRECT_TO
        redirect_pk = collection_pk

        return redirect(redirect_to, redirect_pk)


class FavoriteNFTView(dj_mixins.LoginRequiredMixin, ActionMixin):
    REDIRECT_TO = 'collection details'

    def action(self, request, nft):
        if nft.favorite:
            nft.favorite = False
            nft.nft.likes -= 1
        else:
            nft.favorite = True
            nft.nft.likes += 1

        nft.save()
        nft.nft.save()

        return None

    def get_instance(self, **kwargs):
        try:
            nft_pk = kwargs['pk']
            profile = self.request.user.profile

            instance = profile.favorite_set.get(nft_id=nft_pk)

            return instance
        except dj_exceptions.ObjectDoesNotExist:
            raise dj_http.Http404

    def redirect(self, *args, **kwargs):
        nft_pk = self.kwargs['pk']
        collection_pk = NFT.objects.get(pk=nft_pk).collection.pk

        redirect_to = self.REDIRECT_TO
        redirect_pk = collection_pk

        return redirect(redirect_to, redirect_pk)
