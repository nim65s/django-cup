from django.db import models
from django.contrib.auth.models import User


class Cup(models.Model):
    name = models.DecimalField(max_digits=8, decimal_places=2)
    mini = models.DecimalField(max_digits=8, decimal_places=2)
    maxi = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


class Don(models.Model):
    cup = models.ForeignKey(Cup)
    user = models.ForeignKey(User)
    maxi = models.DecimalField(max_digits=8, decimal_places=2)
    mini = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


    class Meta:
        unique_together = ('cup', 'user')
