from functools import wraps
from django.shortcuts import redirect

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if 'perfil' in request.session and request.session['perfil'] in roles:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/')
        return wrapper
    return decorator
