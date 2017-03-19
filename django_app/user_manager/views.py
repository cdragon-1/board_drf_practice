from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context
from django.template.context_processors import csrf

from django.template.loader import get_template

from post_service.forms import LoginForm


def login(request):
    template = get_template('login_form.html')

    context = Context({'login_form': LoginForm()})
    context.update(csrf(request))

    return HttpResponse(template.render(context))


def login_validate(request):
    login_form_data = LoginForm(request.POST)

    if login_form_data.is_valid():
        user = auth.authenticate(username=login_form_data['id'], password=login_form_data['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)

                return redirect('/board/')
        else:
            return HttpResponse('사용자가 없거나 비밀번호를 잘못 누르셨습니다.')
    else:
        return HttpResponse('로그인 폼이 비정상적입니다.')
