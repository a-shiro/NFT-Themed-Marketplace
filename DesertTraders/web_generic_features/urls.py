from django.urls import path

from DesertTraders.web_generic_features.views.main import HomeView, PrivacyPolicyView, \
    TermsOfServiceView
from DesertTraders.web_generic_features.views.marketplace import MarketplaceView, CollectionDetailsView, buy_nft
from DesertTraders.web_generic_features.views.profile import MyCollectionView, CreateCollectionView, \
    CreateNFTView, mint_collection, ProfileWorkshopView

urlpatterns = [
    # Main tied views
    path('', HomeView.as_view(), name='home'),
    path('privacy-policy', PrivacyPolicyView.as_view(template_name='web_generic_features/main/privacy_policy.html'),
         name='privacy policy'),
    path('terms-of-service', TermsOfServiceView.as_view(template_name='web_generic_features/main/terms_of_service.html'),
         name='terms of service'),

    # Marketplace tied views
    path('marketplace', MarketplaceView.as_view(), name='marketplace'),
    path('collection/details/<int:pk>', CollectionDetailsView.as_view(), name='collection details'),
    path('buy/<int:pk>', buy_nft, name='buy nft'),

    # Profile tied views
    path('profile/<int:pk>/workshop', ProfileWorkshopView.as_view(), name='profile workshop'),
    path('profile/create-collection', CreateCollectionView.as_view(), name='create collection'),
    path('profile/create-nft', CreateNFTView.as_view(), name='create nft'),
    path('mint/<int:pk>', mint_collection, name='mint collection'),

    path('profile/<int:pk>/my-collection', MyCollectionView.as_view(), name='my collection'),
]
