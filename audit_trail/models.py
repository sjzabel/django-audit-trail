from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from duct_tape.models import TimeStampedModelBase

class AuditLog(TimeStampedModelBase):
    #fields that allow for a generic relation
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    log = models.TextField(blank=True)
