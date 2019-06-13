from django.conf.urls import url
from .views import LoginView, UserView, LogoutView, ChangePasswordView, AddUserView, \
    CreateUserListView, DeleteUserView, ChangeDetiails

urlpatterns = [
    url('^me/$', UserView.as_view(), name='me'),
    url('^login/$', LoginView.as_view(), name='login'),
    url('^logout/$', LogoutView.as_view(), name='logout'),
    url('^change_detils/$', ChangeDetiails.as_view(), name='change_details'),
    url('^change_passwd/$', ChangePasswordView.as_view(), name='change_passwd'),
    url('^add_user/$', AddUserView.as_view(), name='add_user'),
    url('^create_user_list/$', CreateUserListView.as_view(), name='create_user_list'),
    url('^del_user/$', DeleteUserView.as_view(), name='del_user'),
]
