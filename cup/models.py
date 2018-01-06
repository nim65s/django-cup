from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from autoslug import AutoSlugField
from ndh.utils import query_sum


class Cup(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    mini = models.DecimalField(max_digits=8, decimal_places=2)
    clos = models.BooleanField(default=False)

    def __str__(self):
        return f'Cup pour {self.name}'

    def get_absolute_url(self):
        return reverse('cup:cup', kwargs={'slug': self.slug})

    def funded(self):
        return query_sum(self.don_set, 'maxi') >= self.mini

    def missing(self):
        return self.mini - query_sum(self.don_set, 'maxi')

    def effort(self):
        mini_sum = query_sum(self.don_set, 'mini')
        maxi_sum = query_sum(self.don_set, 'maxi')
        return (self.mini - mini_sum) / (maxi_sum - mini_sum)


class Don(models.Model):
    cup = models.ForeignKey(Cup, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    maxi = models.DecimalField(max_digits=8, decimal_places=2)
    mini = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f'Don de {self.user.username} pour {self.cup.name}'

    def get_absolute_url(self):
        return self.cup.get_absolute_url()

    class Meta:
        unique_together = ('cup', 'user')

    def pays(self):
        return self.mini + Decimal(self.cup.effort() * (self.maxi - self.mini)).quantize(Decimal('.01'))
