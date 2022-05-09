from django.views import generic as generic_views

from DesertTraders.web_generic_features.models import Profile, Collection, NFT
from DesertTraders.web_generic_features.views.view_helpers.helpers import get_profile_nfts_and_nft_quantity


class PublicProfileWorkshopView(generic_views.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/public_profile/public_workshop.html'

    def get_context_data(self, **kwargs):
        profile_collections = Collection.objects.filter(user=self.object.user, posted_for_sale=True)

        context = super().get_context_data(**kwargs)

        context['profile_collections'] = profile_collections

        return context


class PublicProfileCollectionView(generic_views.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/public_profile/public_collection.html'

    def get_context_data(self, **kwargs):
        profile_nfts_and_nft_quantity = get_profile_nfts_and_nft_quantity(self.object)

        context = super().get_context_data(**kwargs)

        context['profile_nfts_and_nft_quantity'] = profile_nfts_and_nft_quantity

        return context


class PublicProfileFavoriteView(generic_views.DetailView):
    model = Profile
    template_name = 'web_generic_features/profile/public_profile/public_favorite.html'

    def get_context_data(self, **kwargs):
        favorite_nfts = NFT.objects.filter(favorite__profile_id=self.object, favorite__favorite=True)

        context = super().get_context_data(**kwargs)

        context['favorite_nfts'] = favorite_nfts

        return context
