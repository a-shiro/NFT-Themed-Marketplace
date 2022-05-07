from django import views as generic_views
from django.shortcuts import redirect
from django.views.generic import base
from django.views.generic import detail
from django.core import exceptions as django_exceptions

from DesertTraders.users.models import CustomUser
from DesertTraders.web_generic_features.views.view_helpers.helpers import match_users
from DesertTraders.web_generic_features.models import Collection


class SimpleStaticPageMixin(base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['show_footer'] = True
        return context


class CompareUsersMixin(detail.BaseDetailView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                CustomUser.objects.get(pk=kwargs['pk'])  # Checks if the user exists

                current_user_pk = self.request.user.pk
                if match_users(current_user_pk, **kwargs):
                    return redirect('personal profile workshop', pk=kwargs['pk'])
            except django_exceptions.ObjectDoesNotExist:
                return redirect('404')

        return super().get(request, *args, **kwargs)


class CollectionAccessMixin(generic_views.View):
    def dispatch(self, request, *args, **kwargs):
        try:
            collection_owner = Collection.objects.get(pk=kwargs['pk']).user.pk

            if collection_owner != self.request.user.pk:
                raise django_exceptions.BadRequest
        except django_exceptions.BadRequest:
            return redirect('400')

        except django_exceptions.ObjectDoesNotExist:
            return redirect('404')

        return super().dispatch(request, *args, **kwargs)

