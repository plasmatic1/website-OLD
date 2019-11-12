from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit
from django import forms
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import FormView

from view_utils import get_previous_url_as_redirect


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, required=True)
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                'username'
            ),
            Row(
                'password'
            ),
            Submit('submit', 'Login!')
        )


class LoginFormView(FormView):
    template_name = 'main/login.html'
    form_class = LoginForm
    success_url = ''

    def form_valid(self, form):
        post = self.request.POST
        user = authenticate(self.request, username=post['username'], password=post['password'])
        if user:
            login(self.request, user)
            return HttpResponseRedirect(self.request.GET.get('next', '/'))
        messages.warning(self.request, 'Invalid Username/Password!')
        return redirect('login')


def logout_user(req):
    logout(req)
    return get_previous_url_as_redirect(req)


def login_as_guest(req):
    """
    Logins a user as "guest", and creates a guest account if one does not exist
    :param req:
    :return:
    """
    try:
        guest_user = User.objects.get(username='guest')
    except ObjectDoesNotExist:
        messages.info(req, 'No guest user exists! Creating one...')
        guest_user = User(username='guest', password='guest')
        guest_user.save()

    login(req, guest_user)

    return get_previous_url_as_redirect(req)
