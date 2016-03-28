from django.contrib.admin import site

from .models import Cup, Don

site.register(Cup)
site.register(Don)
