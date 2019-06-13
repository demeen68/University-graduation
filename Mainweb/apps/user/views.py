from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm, ResetPasswordForm, AddUserForm
from .models import UserProfile
from django.contrib.auth import login
from utils.user_utils import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from background_ms.views import page_not_fount
from scrapy_app.models import NeedTitleModel
from .utils.email_utils import send_email


class LoginView(View):
    """ Make user login and if web system check user is something strange ,make user login too.
    """

    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {
            'login_form': login_form,
        })

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = UserProfile.objects.filter(username=username)
            if user:
                user = user.get(username=username)
                if user.check_password(password):
                    login(request, user)
                    return HttpResponseRedirect(reverse('index_layout'))

        return render(request, 'login.html', {
            'msg_bad': "用户名或密码错误, 请检查"
        })


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        return HttpResponseRedirect(reverse('user:login'))


class ChangePasswordView(LoginRequiredMixin, View):
    """Change user password
    """

    def post(self, request):
        reset_form = ResetPasswordForm(request.POST)
        if reset_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 == password2:
                user = request.user
                user.password = make_password(password=password1)
                user.save()
                return render(request, 'login.html', {
                    'msg_good': '密码修改成功'
                })
            else:
                err_details = "两次密码不一致"
        else:
            err_details = ""
        return render(request, 'change_details.html', {
            'msg_bad': '密码修改失败  ' + err_details,
        })


class ChangeDetiails(LoginRequiredMixin, View):
    """Get and change user email
    """

    def get(self, request):
        return render(request, 'change_details.html', {
            'user': request.user,
        })

    def post(self, request):
        email = request.POST.get('email', '')
        if email:
            user = request.user
            user.email = email
            user.save()
            return render(request, 'change_details.html', {
                'user': request.user,
                'msg_good': '邮箱修改成功',
            })
        return render(request, 'change_details.html', {
            'user': request.user,
            'msg_bad': '邮箱修改失败',
        })


class UserView(LoginRequiredMixin, View):
    """User personal details
    """

    def get(self, request):
        return render(request, 'me.html', {
            'user': request.user,
        })


class AddUserView(LoginRequiredMixin, View):
    """Super user create other users or create another super user
    """

    def get(self, request):
        user = request.user
        if user.is_staff:
            return render(request, 'add_user.html', {
                'user': user,
            })

    def post(self, request):
        add_user_form = AddUserForm(request.POST)
        if add_user_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 == password2:
                username = request.POST.get('username', '')
                if not UserProfile.objects.filter(username=username):
                    is_staff = request.POST.get('is_staff', '')
                    email = request.POST.get('email', '')
                    user = UserProfile()
                    user.username = username
                    user.password = make_password(password1)
                    user.is_staff = is_staff
                    user.email = email
                    user.create_by = request.user.username
                    user.save()
                    return render(request, 'add_user.html', {
                        'user': request.user,
                        'msg_good': '成功创建 : ' + username,
                    })
                else:
                    err_details = "用户名已存在"
            else:
                err_details = "两次密码输入不一致"
        else:
            err_details = "请仔细填写标点每一项"
        return render(request, 'add_user.html', {
            'user': request.user,
            'msg_bad': '创建失败  ' + err_details,
        })


class CreateUserListView(LoginRequiredMixin, View):
    """Get user list which created by the request.user
    """

    def get(self, request):
        user = request.user
        if user.is_staff:
            create_list = UserProfile.objects.filter(~Q(username=user.username))
            super_user_list = UserProfile.objects.filter(is_staff=1)
            return render(request, 'create_user_list.html', {
                'user': request.user,
                'create_list': create_list,
                'super_user_list': super_user_list,
            })
        return page_not_fount(request)


class DeleteUserView(LoginRequiredMixin, View):
    """Delete a user
    actually any user can use url to delete anyone including
    himself because of the GET method
    """

    def get(self, request):
        user = request.user
        id = request.GET.get('id', '')
        if user.is_staff and id:
            del_user = UserProfile.objects.get(id=id)
            del_user.delete()
            return HttpResponseRedirect(reverse('user:create_user_list'))
        return page_not_fount(request)


class SendKeyWordsEmailView(LoginRequiredMixin, View):
    """When the scrapy finish its job at first , send email to tell user
    """

    def get(self, request):
        need_title_model = NeedTitleModel.objects.filter(
            has_send_email=False, has_get_past_news=True
        )
        need_send_email = need_title_model.values_list('key_words', 'add_user')
        if need_send_email:
            for need_send in need_send_email:
                email = UserProfile.objects.get(username=need_send[1]).email
                send_type = send_email(email, send_type='title', other_details=need_send[0])
                if send_type:
                    # send email success
                    user_has_send_email = need_title_model.filter(add_user=need_send[1])
                    for user in user_has_send_email:
                        user.has_send_email = True
