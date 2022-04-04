from django.views import generic as generic_views


class HomeView(generic_views.TemplateView):
    template_name = 'web_generic_features/main/home.html'


class PrivacyPolicyView(generic_views.TemplateView):
    template_name = 'web_generic_features/main/privacy_policy.html'


class TermsOfServiceView(generic_views.TemplateView):
    template_name = 'web_generic_features/main/terms_of_service.html'

