"""
Update the basic crud models to record events
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson

from audit_trail.models import AuditLog
from audit_trail.lib import get_request_user


class AuditedModelFormMixin(object):
    def form_valid(self, *args, **kwargs):
        # let the processing happen
        print self.object.pk
        created = self.object.pk == None
        rslt = super(AuditedModelFormMixin,self).form_valid(*args,**kwargs)

        # get the object id
        instance = self.object
        info = {
            'instance':instance.__repr__(),
        }

        if not self.request.user.is_anonymous(): 
            info['user_pk']= self.request.user.id
            info['username']= self.request.user.username

        info['updated_fields'] = instance.get_dirty_fields()


        # save the audit
        seria = simplejson.dumps(info, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
        log = AuditLog(content_object=instance, log=seria)
        log.save()

        return rslt

class CreatedByModelMixin(object):
    """
    This is an abstract Model used to provide
        created_by
        has_creator flag (which is used by CreatedByModelFormMixin)
    """
    created_by = models.ForeignKey(User, related_name='+', editable=False, blank=True, null=True)

    # capture which classes signals need to be listening for
    _class_signal_dict = {}

    @classmethod
    def __new__(klass,*args,**kwargs):
        kls = super(CreatedByModelMixin,klass).__new__(klass)
        if not klass in CreatedByModelMixin._class_signal_dict:
            dispatch_uid = "createdbymodelbase_auto_add_creator__%s.%s" % (klass.__module__, klass.__name__)

            # we don't need to keep the dispatch_uid around but it doesn't hurt
            CreatedByModelMixin._class_signal_dict[klass] = dispatch_uid

            #post_save.connect(CreatedByModelMixin.auto_add_creator,sender=klass,weak=False,dispatch_uid=dispatch_uid)

        return kls
    
    @classmethod
    def auto_add_creator(klass,sender,**kwargs):
        instance = kwargs['instance']
        created = kwargs['created']

        user = get_request_user()
        if user:
            instance.created_by = user
            instance.save()

    def has_creator(self):
        return not self.created_by==None
