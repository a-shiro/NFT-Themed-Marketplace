from django import views as dj_views
from django.contrib.auth import mixins as dj_mixins
from django.core import exceptions as dj_exceptions
from django import http as dj_http
from django.views import generic as dj_generic
from django.urls import reverse_lazy

from DesertTraders.web_generic_features.models import Collection
from DesertTraders.web_generic_features.views.helpers import check_if_button_active


class ActionMixin(dj_generic.View):
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_instance(pk=kwargs['pk'])

        self.action(request, instance)

        return self.redirect(*args, **kwargs)

    def get_instance(self, **kwargs):
        pass

    def action(self, request, instance):
        pass

    def redirect(self, *args, **kwargs):
        pass


class CreateViewMixin(dj_mixins.LoginRequiredMixin, dj_generic.CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user

        return kwargs

    def get_context_data(self, **kwargs):
        profile = self.request.user.profile
        add_nft = check_if_button_active(self.request.user)

        context = super().get_context_data()

        context['profile'] = profile
        context['add_nft'] = add_nft

        return context

    def get_success_url(self):
        profile_pk = self.request.user.pk

        return reverse_lazy('profile', kwargs={'pk': profile_pk})


class CollectionContentMixin(dj_generic.DetailView):
    model = Collection

    def get(self, request, *args, **kwargs):
        try:
            collection_pk = kwargs['pk']
            is_posted_for_sale = kwargs['posted_for_sale']

            Collection.objects.get(pk=collection_pk, posted_for_sale=is_posted_for_sale)

            return super().get(request, *args, **kwargs)
        except dj_exceptions.ObjectDoesNotExist:
            raise dj_http.Http404

    def get_context_data(self, **kwargs):
        collection = self.object
        total_nfts = collection.nft_set.all()
        total_nfts_count = len(total_nfts)

        context = super().get_context_data()

        context['collection'] = collection
        context['total_nfts'] = total_nfts
        context['total_nfts_count'] = total_nfts_count

        return context


class OwnerAccessMixin(dj_views.View):
    def dispatch(self, request, *args, **kwargs):
        current_user_pk = self.request.user.pk
        requested_user_pk = self.get_requested_user_pk(pk=kwargs['pk'])

        if requested_user_pk != current_user_pk:
            raise dj_http.Http404

        return super().dispatch(request, *args, **kwargs)

    def get_requested_user_pk(self, **kwargs):
        requested_user_pk = kwargs['pk']

        return requested_user_pk


class ShowFooterMixin(dj_generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['show_footer'] = True
        return context
