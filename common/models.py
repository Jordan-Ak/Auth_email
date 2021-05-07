import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(_('id'), primary_key = True, default = uuid.uuid4)
    date_created = models.DateTimeField(_('date created'), auto_now_add = True)
    date_updated = models.DateTimeField(_('date updated'), auto_now = True)

    class Meta:
        abstract = True