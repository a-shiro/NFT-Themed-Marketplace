from django.shortcuts import redirect
from django.views import generic as generic_views
from django.core import exceptions as django_exceptions

from DesertTraders.web_generic_features.models import Collection


class AbstractCollectionDetailsView(generic_views.DetailView):
    model = Collection

    def get(self, request, *args, **kwargs):
        try:
            Collection.objects.get(pk=kwargs['pk'], posted_for_sale=kwargs['posted_for_sale'])  # Checks if the user exists
        except django_exceptions.ObjectDoesNotExist:
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
