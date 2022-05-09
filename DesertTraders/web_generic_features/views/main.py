from django.shortcuts import render
from django.views import generic as generic_views

from DesertTraders.web_generic_features.views.view_helpers.helpers import get_most_popular
from DesertTraders.web_generic_features.views.view_helpers.mixins import SimpleStaticPageMixin


class HomeView(generic_views.TemplateView):
    template_name = 'web_generic_features/main/home.html'

    def get_context_data(self, **kwargs):
        most_popular_collections = get_most_popular()

        carousel_first_page = most_popular_collections[0:3]
        carousel_second_page = most_popular_collections[3:6]
        carousel_third_page = most_popular_collections[6:9]

        context = super().get_context_data()

        context['carousel_first_page'] = carousel_first_page
        context['carousel_second_page'] = carousel_second_page
        context['carousel_third_page'] = carousel_third_page

        return context


class PrivacyPolicyView(generic_views.TemplateView, SimpleStaticPageMixin):
    template_name = 'web_generic_features/main/privacy_policy.html'


class TermsOfServiceView(generic_views.TemplateView, SimpleStaticPageMixin):
    template_name = 'web_generic_features/main/terms_of_service.html'


def bad_request_view(request):
    return render(request, 'web_generic_features/main/400.html', status=400)


def not_found_view(request):
    return render(request, 'web_generic_features/main/404.html', status=404)
