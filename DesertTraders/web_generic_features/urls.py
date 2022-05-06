from django.urls import path

from DesertTraders.web_generic_features.views.main import HomeView, PrivacyPolicyView, \
    TermsOfServiceView, bad_request_view, not_found_view
from DesertTraders.web_generic_features.views.marketplace import MarketplaceView, CollectionDetailsView, \
    FavoriteNFTView, SortCollectionView, BuyNFTView, SearchMarketplaceView
from DesertTraders.web_generic_features.views.profile.personal import PersonalProfileCollectionView, \
    CreateCollectionView, CreateNFTView, EditProfileView, WorkshopCollectionDetailsView, PersonalProfileFavoriteView, \
    PostOnMarketView, RemoveCollectionView, RemoveNFTView, ProfileView
from DesertTraders.web_generic_features.views.profile.public import PublicProfileCollectionView, \
    PublicProfileFavoriteView

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
    path('buy/<int:pk>', BuyNFTView.as_view(), name='buy nft'),  # Private
    path('favorite/<int:pk>', FavoriteNFTView.as_view(), name='favorite nft'),  # Private
    path('sort/<int:pk>', SortCollectionView.as_view(), name='sort collection'),  # Private
    path('search', SearchMarketplaceView.as_view(), name='search marketplace'),  # Private

    # Personal Profile tied urls
    path('profile/<int:pk>/workshop', ProfileView.as_view(), name='profile'),

    path('profile/<int:pk>/collection', PersonalProfileCollectionView.as_view(), name='personal profile collection'),
    path('profile/<int:pk>/workshop/collection', WorkshopCollectionDetailsView.as_view(), name='workshop collection'),
    path('profile/<int:pk>/favorites', PersonalProfileFavoriteView.as_view(), name='personal profile favorites'),

    path('profile/<int:pk>/edit', EditProfileView.as_view(), name='edit profile'),  # Private

    path('profile/create-collection', CreateCollectionView.as_view(), name='create collection'),  # Private
    path('profile/create-nft', CreateNFTView.as_view(), name='create nft'),  # Private
    path('sell/<int:pk>', PostOnMarketView.as_view(), name='sell collection'),  # Private
    path('remove/<int:pk>', RemoveCollectionView.as_view(), name='remove collection'),  # Private
    path('remove/nft/<int:pk>', RemoveNFTView.as_view(), name='remove nft'),  # Private

    # Public Profile tied urls
    path('public-profile/<int:pk>/collection', PublicProfileCollectionView.as_view(), name='public collection'),
    path('public-profile/<int:pk>/favorites', PublicProfileFavoriteView.as_view(), name='public favorites'),
]
