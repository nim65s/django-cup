from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, RedirectView, UpdateView
from django.views.generic.detail import SingleObjectMixin

from .models import Cup, Don


class CupCreateView(LoginRequiredMixin, CreateView):
    model = Cup
    fields = ['name', 'mini']


class DonDispatchView(LoginRequiredMixin, SingleObjectMixin, RedirectView):
    model = Cup

    def get_redirect_url(self, *args, **kwargs):
        cup = self.get_object()
        if cup.don_set.filter(user=self.request.user).exists():
            self.kwargs['pk'] = cup.don_set.filter(user=self.request.user).first().pk
            return reverse('cup:update_don', kwargs=self.kwargs)
        return reverse('cup:add_don', kwargs=self.kwargs)


class DonMixin(LoginRequiredMixin):
    model = Don
    fields = ['maxi', 'mini']

    def form_valid(self, form):
        form.instance.cup = get_object_or_404(Cup, slug=self.kwargs['slug'])
        form.instance.user = self.request.user
        return super().form_valid(form)


class DonCreateView(DonMixin, CreateView):
    pass


class DonUpdateView(DonMixin, UpdateView):
    pass
