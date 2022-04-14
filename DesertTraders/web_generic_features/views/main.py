from django.shortcuts import render
from django.views import generic as generic_views

from DesertTraders.web_generic_features.mixins import SimpleStaticPageMixin


class HomeView(generic_views.TemplateView):
    template_name = 'web_generic_features/main/home.html'


class PrivacyPolicyView(generic_views.TemplateView, SimpleStaticPageMixin):
    template_name = 'web_generic_features/main/privacy_policy.html'


class TermsOfServiceView(generic_views.TemplateView, SimpleStaticPageMixin):
    template_name = 'web_generic_features/main/terms_of_service.html'


def bad_request_view(request):
    return render(request, 'web_generic_features/main/400.html', status=400)


def not_found_view(request):
    return render(request, 'web_generic_features/main/404.html', status=404)
