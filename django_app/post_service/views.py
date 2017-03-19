from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import Context
from django.template.context_processors import csrf

from django.template.loader import get_template
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from post_service.forms import LoginForm
from post_service.models import Post


def post_list(request):
    template = get_template('post_list.html')

    page_data = Paginator(Post.objects.all(), 3)
    page = request.GET.get('page')

    if page is None:
        page = 1

    try:
        posts = page_data.page(page)
    except PageNotAnInteger:
        posts = page_data.page(1)
    except EmptyPage:
        posts = page_data.page(page_data.num_pages)

    context = Context({'post_list': posts, 'current_page': int(page), 'total_page': range(1, page_data.num_pages + 1)})

    return HttpResponse(template.render(context))


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
