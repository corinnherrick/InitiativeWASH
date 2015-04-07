# gsteway/admin.py

from django.contrib import admin

from .models import Neighborhood
from .models import Source
from .models import Test
from .models import TestResult

admin.site.register(Neighborhood)
admin.site.register(Source)
admin.site.register(Test)
admin.site.register(TestResult)
