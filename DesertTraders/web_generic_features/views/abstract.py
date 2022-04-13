from django.views import generic as generic_views
from django.core import exceptions as django_exceptions
from django import http


from DesertTraders.web_generic_features.helpers import get_collection_with_pk
from DesertTraders.web_generic_features.models import Collection, NFT


class AbstractCollectionDetailsView(generic_views.TemplateView):
    def get(self, request, *args, **kwargs):
        try:
            Collection.objects.get(pk=kwargs['pk'], posted_for_sale=kwargs['posted_for_sale'])
        except django_exceptions.ObjectDoesNotExist:
            raise http.Http404('Does not exist.')  # Return Custom 404 Page

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        collection = get_collection_with_pk(**kwargs)
        total_nfts = NFT.objects.filter(collection=collection)
        total_nfts_count = len(total_nfts)

        context = super().get_context_data()

        context['collection'] = collection
        context['total_nfts'] = total_nfts
        context['total_nfts_count'] = total_nfts_count

        return context
