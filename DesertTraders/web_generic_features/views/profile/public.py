from django.views import generic as dj_generic

from DesertTraders.web_generic_features.models import Profile, Collection, NFT
from DesertTraders.web_generic_features.views.helpers import get_nfts_and_quantity


class PublicProfileWorkshopView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/public/public_workshop.html'

    def get_context_data(self, **kwargs):
        collections = Collection.objects.filter(user=self.object.user, posted_for_sale=True)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections

        return context


class PublicProfileCollectionView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/public/public_collection.html'

    def get_context_data(self, **kwargs):
        nft_and_quantity_pair = get_nfts_and_quantity(self.object)

        context = super().get_context_data(**kwargs)

        context['nft_and_quantity_pair'] = nft_and_quantity_pair

        return context


class PublicProfileFavoriteView(dj_generic.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/public/public_favorite.html'

    def get_context_data(self, **kwargs):
        favorite_nfts = NFT.objects.filter(favorite__profile_id=self.object, favorite__favorite=True)

        context = super().get_context_data(**kwargs)

        context['favorite_nfts'] = favorite_nfts

        return context
