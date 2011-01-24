from django.db.models.signals import post_save, post_delete

from duct_tape.models import DirtyModelMixin

from audit_trail.receivers import post_save_receiver, post_delete_receiver

def register_for_audit(model_klass):
    '''
    Register a model class for  post_save and post_delete
    '''
    signals =[]

    #add DirtyModelMixin so we can tell which fields have changed on edit
    if not DirtyModelMixin in model_klass.__bases__:
        model_klass.__bases__ = (DirtyModelMixin,) + model_klass.__bases__

    post_save.connect(receiver=post_save_receiver,
            sender=model_klass,dispatch_uid="audit_trail_post_save_receiver_%s" % model_klass)

    post_delete.connect(receiver=post_delete_receiver,
            sender=model_klass,dispatch_uid="audit_trail_post_delete_receiver_%s" % model_klass)

    return model_klass
