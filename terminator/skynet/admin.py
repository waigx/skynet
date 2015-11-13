from django.contrib import admin
from .models import *


class TopDomainAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'is_leak', 'accept_count', 'reject_count']
    fieldsets = [
        ('Domain Name', {'fields': ['domain_name']}),
        ('Leaked', {'fields': ['is_leak']}),
        ('Accepted', {'fields': ['accept_count']}),
        ('Rejected', {'fields': ['reject_count']}),
    ]


class FullRequestAdmin(admin.ModelAdmin):
    list_display = ['page_url', 'is_leak', 'accept_count', 'reject_count', 'top_domain_name']
    fieldsets = [
        ('Request URL', {'fields': ['page_url']}),
        ('Leaked', {'fields': ['is_leak']}),
        ('Accepted', {'fields': ['accept_count']}),
        ('Rejected', {'fields': ['reject_count']}),
        ('Top Domain', {'fields': ['top_domain']}),
    ]

    def top_domain_name(self, obj):
        return obj.top_domain.domain_name


class LeakedToURLAdmin(admin.ModelAdmin):
    list_display = ['leak_url', 'leak_type', 'leak_from_domain']
    fieldsets = [
        ('Leak To', {'fields': ['leak_url']}),
        ('Leak Type', {'fields': ['leak_type']}),
        ('Leak From', {'fields': ['leak_from_domain']}),
    ]

    def leak_from_domain(self, obj):
        return obj.leak_from.page_url


admin.site.register(TopDomain, TopDomainAdmin)
admin.site.register(FullRequest, FullRequestAdmin)
admin.site.register(LeakToURL, LeakedToURLAdmin)
