from django.shortcuts import redirect
def login_yz(func):
    def func1(request,*args,**kwargs):
        if request.session.has_key('uid'):
            return func(request,*args,**kwargs)
        else:
            return redirect('/login/')

    return func1