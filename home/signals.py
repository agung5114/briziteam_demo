from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .logging import user_log
 
 
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    user_log(str(user),'login')
    print('user logged in')
 
 
# @receiver(user_login_failed)
# def log_user_login_failed(sender, credentials, request, **kwargs):
#     # create_userlog(str(user),'login failed')
#     print('user logged in failed')
 
 
@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    user_log(str(user),'logout')
    print('user logged out')