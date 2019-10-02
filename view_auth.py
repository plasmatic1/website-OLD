from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit
from django import forms
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect
from django.views.generic import FormView


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
            return redirect('main:index')
        messages.warning(self.request, 'Invalid Username/Password!')
        return redirect('login')


def logout_user(req):
    logout(req)
    return redirect('main:index')
