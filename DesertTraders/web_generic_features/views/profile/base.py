from django.views import generic as dj_generic

from DesertTraders.web_generic_features.views.profile.personal import PersonalProfileWorkshopView, \
    PersonalProfileCollectionView, PersonalProfileFavoriteView
from DesertTraders.web_generic_features.views.profile.public import PublicProfileWorkshopView, \
    PublicProfileCollectionView, PublicProfileFavoriteView


class ProfileView(dj_generic.View):
    def dispatch(self, request, *args, **kwargs):
        current_user_pk = self.request.user.pk
        searched_user_pk = kwargs['pk']

        if current_user_pk != searched_user_pk:
            return PublicProfileWorkshopView.as_view()(self.request, pk=kwargs['pk'])
        return PersonalProfileWorkshopView.as_view()(self.request, pk=kwargs['pk'])


class ProfileCollectionView(dj_generic.View):
    def dispatch(self, request, *args, **kwargs):
        current_user_pk = self.request.user.pk
        searched_user_pk = kwargs['pk']

        if current_user_pk != searched_user_pk:
            return PublicProfileCollectionView.as_view()(self.request, pk=kwargs['pk'])
        return PersonalProfileCollectionView.as_view()(self.request, pk=kwargs['pk'])


class ProfileFavoriteView(dj_generic.View):
    def dispatch(self, request, *args, **kwargs):
        current_user_pk = self.request.user.pk
        searched_user_pk = kwargs['pk']

        if current_user_pk != searched_user_pk:
            return PublicProfileFavoriteView.as_view()(self.request, pk=kwargs['pk'])
        return PersonalProfileFavoriteView.as_view()(self.request, pk=kwargs['pk'])
