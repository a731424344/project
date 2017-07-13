class UrlMiddleware:
    def process_view(self,request,view_func,view_args,view_kwargs):

        if request.path not in [
            '/login/','/login_handle/','/register/','/change_pwd/','/suc_reg/',
            '/logout/','/newpwd/','/re_name/','/verify/','/newpwd_handle/','/change_pwd/',
            '/islogin/',
        ]:
            request.session['url_path'] = request.get_full_path()