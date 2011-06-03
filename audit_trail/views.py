"""
Update the basic crud models to record events
"""
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson

from audit_trail.models import AuditLog


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


        
