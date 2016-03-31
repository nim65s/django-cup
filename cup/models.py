from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.functions import Coalesce

from autoslug import AutoSlugField


def query_sum(queryset, field='maxi'):
    return queryset.aggregate(s=Coalesce(models.Sum(field), 0))['s']


class Cup(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    mini = models.DecimalField(max_digits=8, decimal_places=2)
    clos = models.BooleanField(default=False)

    def __str__(self):
        return 'Cup pour %s' % self.name

    def get_absolute_url(self):
        return reverse('cup:cup', kwargs={'slug': self.slug})

    def funded(self):
        return query_sum(self.don_set) >= self.mini

    def missing(self):
        return self.mini - query_sum(self.don_set)

    def effort(self):
        mini_sum = query_sum(self.don_set, 'mini')
        maxi_sum = query_sum(self.don_set, 'maxi')
        return (self.mini - mini_sum) / (maxi_sum - mini_sum)


class Don(models.Model):
    cup = models.ForeignKey(Cup)
    user = models.ForeignKey(User)
    maxi = models.DecimalField(max_digits=8, decimal_places=2)
    mini = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return 'Don de %s pour %s' % (self.user.username, self.cup.name)

    def get_absolute_url(self):
        return self.cup.get_absolute_url()

    class Meta:
        unique_together = ('cup', 'user')

    def pays(self):
        return self.mini + Decimal(self.cup.effort() * (self.maxi - self.mini)).quantize(Decimal('.01'))
