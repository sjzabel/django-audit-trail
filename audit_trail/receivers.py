from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.utils import simplejson

from audit_trail.models import AuditLog
import sys, itertools

def get_request_user():
    '''
    blindly walks up the stack looking for 
    request.user
    '''
    for i in itertools.count():
        frame = sys._getframe(i)
        if not frame: return False
        if "request" in frame.f_locals:
            request = frame.f_locals['request']
            if not hasattr(request,"user"):
                '''
                wrong signature... keep looking
                '''
                continue
            if not request.user.is_authenticated(): return False
            return request.user

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
