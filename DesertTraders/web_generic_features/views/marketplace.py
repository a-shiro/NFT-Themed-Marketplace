from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic as generic_views

from DesertTraders.web_generic_features.helpers import get_collections_on_market, transaction, get_nft_with_pk
from DesertTraders.web_generic_features.models import Profile
from DesertTraders.web_generic_features.views.abstract import AbstractCollectionDetailsView


class MarketplaceView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/marketplace.html'

    def get_context_data(self, **kwargs):
        total_collections = get_collections_on_market()
        total_collections_count = len(total_collections)

        context = super().get_context_data(**kwargs)

        context['total_collections'] = total_collections
        context['total_collections_count'] = total_collections_count
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
    nft = get_nft_with_pk(pk=pk)

    transaction(profile, nft)

    return redirect('collection details', nft.collection.pk)
