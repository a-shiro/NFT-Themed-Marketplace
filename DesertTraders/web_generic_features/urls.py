from django.urls import path

from DesertTraders.web_generic_features.views.main import HomeView, PrivacyPolicyView, \
    TermsOfServiceView
from DesertTraders.web_generic_features.views.marketplace import MarketplaceView, CollectionDetailsView, buy_nft
from DesertTraders.web_generic_features.views.profile import PersonalCollectionView, CreateCollectionView, \
    CreateNFTView, mint_collection, PersonalProfileView, PublicProfileView, PublicProfileCollectionView, \
    remove_collection, EditProfileView, WorkshopCollectionDetailsView, remove_nft

urlpatterns = [
    # Main tied urls
    path('', HomeView.as_view(), name='home'),
    path('privacy-policy', PrivacyPolicyView.as_view(template_name='web_generic_features/main/privacy_policy.html'),
         name='privacy policy'),
    path('terms-of-service',
         TermsOfServiceView.as_view(template_name='web_generic_features/main/terms_of_service.html'),
         name='terms of service'),

    # Marketplace tied urls
    path('marketplace', MarketplaceView.as_view(), name='marketplace'),
    path('collection/details/<int:pk>', CollectionDetailsView.as_view(), name='collection details'),
    path('buy/<int:pk>', buy_nft, name='buy nft'),

    # Personal Profile tied urls
    path('profile/<int:pk>/workshop', PersonalProfileView.as_view(), name='personal profile'),
    path('profile/<int:pk>/workshop/collection', WorkshopCollectionDetailsView.as_view(), name='workshop collection'),
    path('profile/<int:pk>/collection', PersonalCollectionView.as_view(), name='personal collection'),

    path('profile/<int:pk>/edit', EditProfileView.as_view(), name='edit profile'),

    path('profile/create-collection', CreateCollectionView.as_view(), name='create collection'),
    path('profile/create-nft', CreateNFTView.as_view(), name='create nft'),
    path('mint/<int:pk>', mint_collection, name='mint collection'),
    path('remove/<int:pk>', remove_collection, name='remove collection'),
    path('remove/nft/<int:pk>', remove_nft, name='remove nft'),

    # Public Profile tied urls
    path('public-profile/<int:pk>/workshop', PublicProfileView.as_view(), name='public profile'),
    path('public-profile/<int:pk>/collection', PublicProfileCollectionView.as_view(), name='public collection'),

]
