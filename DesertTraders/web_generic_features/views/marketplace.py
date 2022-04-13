from django.contrib.auth.decorators import login_required
from django.core import exceptions as django_exceptions
from django import http
from django.shortcuts import redirect
from django.views import generic as generic_views

from DesertTraders.web_generic_features.helpers import get_collection_with_pk, get_collections_on_market, transaction
from DesertTraders.web_generic_features.models import NFT, Profile, Collection


class MarketplaceView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/marketplace.html'

    def get_context_data(self, **kwargs):
        total_collections = get_collections_on_market()
        total_collections_count = len(total_collections)

        context = super().get_context_data(**kwargs)

        context['total_collections'] = total_collections
        context['total_collections_count'] = total_collections_count
        return context


class CollectionDetailsView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/collection_details.html'

    def get(self, request, *args, **kwargs):
        try:
            Collection.objects.get(pk=kwargs['pk'], posted_for_sale=True)
        except django_exceptions.ObjectDoesNotExist:
            raise http.Http404('Does not exist.')  # Return Custom 404 Page

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        collection = get_collection_with_pk(**kwargs)
        total_nfts = NFT.objects.filter(collection=collection)
        total_nfts_count = len(total_nfts)

        context = super().get_context_data()

        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile

        context['collection'] = collection
        context['total_nfts'] = total_nfts
        context['total_nfts_count'] = total_nfts_count

        return context


@login_required
def buy_nft(request, pk):
    profile = Profile.objects.get(user=request.user)
    nft = NFT.objects.get(pk=pk)

    transaction(profile, nft)

    return redirect('collection details', nft.collection.pk)
