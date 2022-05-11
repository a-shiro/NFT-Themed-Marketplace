from django.urls import path

from DesertTraders.web_generic_features.views.main import HomeView, PrivacyPolicyView, TermsOfServiceView
from DesertTraders.web_generic_features.views.marketplace import MarketplaceView, CollectionDetailsView, \
    FavoriteNFTView, SortCollectionView, BuyNFTView, SearchMarketplaceView
from DesertTraders.web_generic_features.views.profile.personal import CreateCollectionView, CreateNFTView, \
    EditProfileView, PersonalProfileCollectionDetailsView, SellOnMarketView, RemoveCollectionView, \
    RemoveNFTView
from DesertTraders.web_generic_features.views.profile.dispatchers import ProfileView, ProfileCollectionView, \
    ProfileFavoriteView

urlpatterns = [
    # Main
    path('', HomeView.as_view(), name='home'),
    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy policy'),
    path('terms-of-service', TermsOfServiceView.as_view(), name='terms of service'),

    # Marketplace
    path('marketplace', MarketplaceView.as_view(), name='marketplace'),
    path('search', SearchMarketplaceView.as_view(), name='search marketplace'),
    path('collection/details/<int:pk>', CollectionDetailsView.as_view(), name='collection details'),

    path('sort/<int:pk>', SortCollectionView.as_view(), name='sort collection'),
    path('favorite/<int:pk>', FavoriteNFTView.as_view(), name='favorite nft'),
    path('buy/<int:pk>', BuyNFTView.as_view(), name='buy nft'),

    # Profile
    path('profile/<int:pk>/workshop', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/collection', ProfileCollectionView.as_view(), name='profile collection'),
    path('profile/<int:pk>/favorites', ProfileFavoriteView.as_view(), name='profile favorite'),

    # Personal Profile
    path('profile/workshop/collection/details/<int:pk>', PersonalProfileCollectionDetailsView.as_view(),
         name='personal collection details'),
    path('profile/<int:pk>/edit', EditProfileView.as_view(), name='edit profile'),

    path('profile/create-collection', CreateCollectionView.as_view(), name='create collection'),
    path('remove/<int:pk>', RemoveCollectionView.as_view(), name='remove collection'),
    path('sell/<int:pk>', SellOnMarketView.as_view(), name='sell collection'),

    path('profile/create-nft', CreateNFTView.as_view(), name='create nft'),
    path('remove/nft/<int:pk>', RemoveNFTView.as_view(), name='remove nft'),
]
