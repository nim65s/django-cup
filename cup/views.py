from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cup, Don


class DonCreateView(LoginRequiredMixin, CreateView):
    model = Don
    fields = ['maxi', 'mini']

    def form_valid(self, form):
        form.instance.cup = get_object_or_404(Cup, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        return super().form_valid(form)
