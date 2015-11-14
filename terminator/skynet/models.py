from django.db import models


class TopDomain(models.Model):
    domain_name = models.URLField()
    is_leak = models.BooleanField(default=False)
    accept_count = models.PositiveIntegerField(default=0)
    reject_count = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.domain_name

    def __str__(self):
        return self.domain_name


class FullRequest(models.Model):
    page_url = models.URLField()
    is_leak = models.BooleanField(default=False)
    accept_count = models.PositiveIntegerField(default=0)
    reject_count = models.PositiveIntegerField(default=0)
    top_domain = models.ForeignKey(TopDomain, default=None, null=True)

    def __unicode__(self):
        return self.page_url

    def __str__(self):
        return self.page_url


class LeakToURL(models.Model):
    leak_url = models.URLField()
    leak_type = models.PositiveSmallIntegerField(default=0)
    leak_from = models.ForeignKey(FullRequest, default=None, null=True)
