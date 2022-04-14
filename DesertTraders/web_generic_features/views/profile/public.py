from django.views import generic as generic_views

from DesertTraders.web_generic_features.helpers import get_profile_nfts_and_nft_quantity
from DesertTraders.web_generic_features.mixins import CompareUsersMixin
from DesertTraders.web_generic_features.models import Profile, Collection


class PublicProfileWorkshopView(generic_views.DetailView, CompareUsersMixin):
    template_name = 'web_generic_features/profile/public_profile/public_workshop.html'
    model = Profile

    def get_context_data(self, **kwargs):
        profile_collections = Collection.objects.filter(user=self.object.user, posted_for_sale=True)

        context = super().get_context_data(**kwargs)

        context['profile_collections'] = profile_collections
        return context


class PublicProfileCollectionView(generic_views.DetailView, CompareUsersMixin):
    template_name = 'web_generic_features/profile/public_profile/public_collection.html'
    model = Profile

    def get_context_data(self, **kwargs):
        profile_nfts_and_nft_quantity = get_profile_nfts_and_nft_quantity(self.object)

        context = super().get_context_data(**kwargs)

        context['profile_nfts_and_nft_quantity'] = profile_nfts_and_nft_quantity

        return context
