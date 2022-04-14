from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic as generic_views
from django.core import exceptions as django_exceptions

from DesertTraders.web_generic_features.helpers import transaction, validate_info
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
        return super().get_context_data(**kwargs)


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
