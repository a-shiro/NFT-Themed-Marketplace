from django.views.generic import base


# For main views
class SimpleStaticPageMixin(base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['show_footer'] = True
        return context