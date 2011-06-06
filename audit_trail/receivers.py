from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson

from audit_trail.models import AuditLog
from audit_trail.lib import get_request_user

def post_save_receiver(sender,**kwargs):
    instance = kwargs['instance']
    print 

    info = {
        'instance':instance.__repr__(),
    }

    user = get_request_user()
    if user:
        info['user_pk']= user.id
        info['username']= user.username

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
        'instance':instance.__repr__(),
        'action':'delete',
    }

    user = get_request_user()
    if user:
        info['user_pk']= user.id
        info['username']= user.username

    seria = simplejson.dumps(info, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)
    log = AuditLog(content_object=instance, log=seria)
    log.save()
