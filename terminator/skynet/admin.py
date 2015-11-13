from django.contrib import admin
from .models import *

admin.site.register(TopDomain)
admin.site.register(FullRequest)
admin.site.register(LeakToURL)
