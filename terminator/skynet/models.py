from django.db import models


class TopDomain(models.Model):
    domain_name = models.URLField()
    accept_count = models.PositiveIntegerField(default=0)
    reject_count = models.PositiveIntegerField(default=0)


class FullRequest(models.Model):
    page_url = models.URLField()
    accept_count = models.PositiveIntegerField(default=0)
    reject_count = models.PositiveIntegerField(default=0)
    top_domain = models.ForeignKey(TopDomain, default=None)

    @property
    def __str__(self):
        return self.page_url


class LeakToURL(models.Model):
    leak_url = models.URLField()
    leak_type = models.PositiveSmallIntegerField()
    leak_from = models.ForeignKey(FullRequest)

    @property
    def __str__(self):
        return self.leak_url

