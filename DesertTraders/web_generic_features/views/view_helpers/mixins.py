from django import views as dj_views
from django.contrib.auth import mixins as dj_mixins
from django.core import exceptions as dj_exceptions
from django.views import generic as dj_generic
from django.urls import reverse_lazy
from django.shortcuts import redirect

from DesertTraders.web_generic_features.models import Collection


class ActionMixin(dj_generic.View, dj_mixins.LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        action = kwargs['action']
        instance = kwargs['instance']

        action(request, instance)

    def redirect(self, *args, **kwargs):
        return redirect('profile', self.request.user.pk)


class CreateViewMixin(dj_generic.CreateView, dj_mixins.LoginRequiredMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        kwargs['user'] = self.request.user

        return kwargs

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.pk})


class CollectionContentMixin(dj_generic.DetailView):
    model = Collection

    def get(self, request, *args, **kwargs):
        try:
            Collection.objects.get(pk=kwargs['pk'],
                                   posted_for_sale=kwargs['posted_for_sale'])  # Checks if the user exists
        except dj_exceptions.ObjectDoesNotExist:
            return redirect('404')  # Return Custom 404 Page

        return super().get(request, *args, **kwargs)

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
        try:
            collection_owner = Collection.objects.get(pk=kwargs['pk']).user.pk

            if collection_owner != self.request.user.pk:
                raise dj_exceptions.BadRequest
        except dj_exceptions.BadRequest:
            return redirect('400')

        except dj_exceptions.ObjectDoesNotExist:
            return redirect('404')

        return super().dispatch(request, *args, **kwargs)


class SimpleStaticPageMixin(dj_generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['show_footer'] = True
        return context
