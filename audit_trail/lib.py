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
