from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.views import generic as generic_views

from DesertTraders.web_generic_features.helpers import get_tuple_collection_with_profile
from DesertTraders.web_generic_features.models import Collection, NFT, Profile, Collected


class MarketplaceView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/marketplace.html'

    def get_context_data(self, **kwargs):
        collection_profile_pair = get_tuple_collection_with_profile()
        collections_count = len(Collection.objects.filter(posted_for_sale=True))

        context = super().get_context_data(**kwargs)

        context['collections_count'] = collections_count
        context['collection_profile_pair'] = collection_profile_pair
        context['hide_footer'] = True
        return context


class CollectionDetailsView(generic_views.TemplateView):
    template_name = 'web_generic_features/marketplace/collection_details.html'

    def get_context_data(self, **kwargs):
        collection = Collection.objects.filter(pk=self.kwargs['pk'])[0]
        nfts = NFT.objects.filter(collection=collection)
        nfts_count = len(nfts)

        context = super().get_context_data()

        context['collection'] = collection
        context['nfts'] = nfts
        context['nfts_count'] = nfts_count
        context['hide_footer'] = True
        if self.request.user.is_authenticated:
            profile = Profile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context


@login_required
def buy_nft(request, pk):
    profile = Profile.objects.get(user=request.user)
    nft = NFT.objects.get(pk=pk)

    if nft in profile.my_collection.all():
        collected_nft = Collected.objects.filter(profile=profile, NFT=nft).first()
        collected_nft.quantity += 1
        collected_nft.save()
    else:
        profile_collection = Collected(profile=profile, NFT=nft)
        profile_collection.save()

    nft.quantity -= 1
    nft.save()
    return redirect('marketplace')
