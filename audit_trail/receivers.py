from user_registry import UserRegistry
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson

from audit_trail.models import AuditLog

def post_save_receiver(sender,**kwargs):
    instance = kwargs['instance']

    info = {
        'user':0,
        'instance':instance.__repr__(),
    }

    if UserRegistry.has_user(): 
        info['user']= UserRegistry.get_user().id

    if kwargs['created']:
        info['action'] = 'create'
        info['fields'] = instance.get_dirty_fields()
    else:
        info['action'] = 'edit'
        info['updated_fields'] = instance.get_dirty_fields()

    seria = simplejson.dumps(info, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
    log = AuditLog(content_object=instance, log=seria)
    log.save()

def post_delete_receiver(sender,**kwargs):
    instance = kwargs['instance']

    info = {
        'user':0,
        'instance':instance.__repr__(),
        'action':'delete',
    }

    if UserRegistry.has_user(): 
        info['user']= UserRegistry.get_user().id

    seria = simplejson.dumps(info, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
    log = AuditLog(content_object=instance, log=seria)
    log.save()
