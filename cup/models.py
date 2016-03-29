from django.db import models
from django.db.models.functions import Coalesce

from django.contrib.auth.models import User


def query_sum(queryset, field='maxi'):
    return queryset.aggregate(s=Coalesce(models.Sum(field), 0))['s']


class Cup(models.Model):
    name = models.CharField(max_length=200, unique=True)
    mini = models.DecimalField(max_digits=8, decimal_places=2)
    maxi = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    clos = models.BooleanField(default=False)

    def __str__(self):
        return 'Cup pour %s' % self.name

    def get_absolute_url(self):
        ...

    def funded(self):
        return query_sum(self.don_set) >= self.mini

    def missing(self):
        return self.mini - query_sum(self.don_set)


class Don(models.Model):
    cup = models.ForeignKey(Cup)
    user = models.ForeignKey(User)
    maxi = models.DecimalField(max_digits=8, decimal_places=2)
    mini = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return 'Don de %s pour %s' % (self.user.username, self.cup.name)

    class Meta:
        unique_together = ('cup', 'user')
