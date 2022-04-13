from django.shortcuts import redirect
from django.views import generic as generic_views

from DesertTraders.web_generic_features.helpers import users_match, get_collections_on_market, \
    get_profile_nfts_and_nft_quantity
from DesertTraders.web_generic_features.models import Profile


class PublicProfileView(generic_views.DetailView):
    template_name = 'web_generic_features/profile/public_profile/public_workshop.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            session_user_pk = int(self.request.session.get('_auth_user_id'))
            if users_match(session_user_pk, **kwargs):
                return redirect('personal profile workshop', pk=kwargs['pk'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        collections = get_collections_on_market().filter(user=self.object.user)

        context = super().get_context_data(**kwargs)

        context['collections'] = collections
        return context


class PublicProfileCollectionView(generic_views.DetailView):
    template_name = 'web_generic_features/profile/public_profile/public_collection.html'
    model = Profile

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            session_user_pk = int(self.request.session.get('_auth_user_id'))
            if users_match(session_user_pk, **kwargs):
                return redirect('personal profile workshop', pk=kwargs['pk'])

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        profile_nfts_and_nft_quantity = get_profile_nfts_and_nft_quantity(self.object)

        context = super().get_context_data(**kwargs)

        context['profile_nfts_and_nft_quantity'] = profile_nfts_and_nft_quantity

        return context
