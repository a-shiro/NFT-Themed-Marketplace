from django.urls import path

from DesertTraders.web_generic_features.views.main import HomeView, PrivacyPolicyView, \
    TermsOfServiceView, bad_request_view, not_found_view
from DesertTraders.web_generic_features.views.marketplace import MarketplaceView, CollectionDetailsView, buy_nft, \
    FavoriteNFTView
from DesertTraders.web_generic_features.views.profile.personal import PersonalProfileCollectionView, \
    CreateCollectionView, \
    CreateNFTView, post_on_market, PersonalProfileWorkshopView, remove_collection, EditProfileView, \
    WorkshopCollectionDetailsView, remove_nft, PersonalProfileFavoriteView
from DesertTraders.web_generic_features.views.profile.public import PublicProfileWorkshopView, \
    PublicProfileCollectionView, PublicProfileFavoriteView

urlpatterns = [
    # Main tied urls
    path('', HomeView.as_view(), name='home'),  # Public
    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy policy'),  # Public
    path('terms-of-service', TermsOfServiceView.as_view(), name='terms of service'),  # Public
    path('bad-request', bad_request_view, name='400'),  # Public
    path('not-found', not_found_view, name='404'),  # Public

    # Marketplace tied urls
    path('marketplace', MarketplaceView.as_view(), name='marketplace'),  # Public
    path('collection/details/<int:pk>', CollectionDetailsView.as_view(), name='collection details'),  # Public
    path('buy/<int:pk>', buy_nft, name='buy nft'),  # Private
    path('favorite/<int:pk>', FavoriteNFTView.as_view(), name='favorite nft'),  # Private

    # Personal Profile tied urls
    path('profile/<int:pk>/workshop', PersonalProfileWorkshopView.as_view(), name='personal profile workshop'),  # Private
    path('profile/<int:pk>/collection', PersonalProfileCollectionView.as_view(), name='personal profile collection'),  # Private
    path('profile/<int:pk>/workshop/collection', WorkshopCollectionDetailsView.as_view(), name='workshop collection'),  # Private
    path('profile/<int:pk>/favorites', PersonalProfileFavoriteView.as_view(), name='personal profile favorites'),

    path('profile/<int:pk>/edit', EditProfileView.as_view(), name='edit profile'),  # Private

    path('profile/create-collection', CreateCollectionView.as_view(), name='create collection'), # Private
    path('profile/create-nft', CreateNFTView.as_view(), name='create nft'),  # Private
    path('sell/<int:pk>', post_on_market, name='sell collection'),  # Private
    path('remove/<int:pk>', remove_collection, name='remove collection'),  # Private
    path('remove/nft/<int:pk>', remove_nft, name='remove nft'),  # Private

    # Public Profile tied urls
    path('public-profile/<int:pk>/workshop', PublicProfileWorkshopView.as_view(), name='public profile'),  # Public
    path('public-profile/<int:pk>/collection', PublicProfileCollectionView.as_view(), name='public collection'),  # Public
    path('public-profile/<int:pk>/favorites', PublicProfileFavoriteView.as_view(), name='public favorites'),
    # Public

]


