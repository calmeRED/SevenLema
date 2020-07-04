from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from cmdb.models.shop import Shop
from cmdb.models.user import User


@require_GET
def root(request):
    return redirect('/index/')


@require_GET
def register(request):
    return render(request, 'register.html')


@require_GET
def login(request):
    if 'id' in request.session:
        return redirect('/')
    else:
        return render(request, 'login.html')


def get_login_context(request):
    if 'id' in request.session:
        return dict(model_to_dict(User.objects.get(id=request.session['id']).items()) + {'login': True}.items())
    else:
        return {'login': False}


@require_GET
def shop(request):
    return render(request, 'shop.html', get_login_context(request))


@require_GET
def dish(request, shop_id):
    ctx = get_login_context(request)
    try:
        ctx['shop_obj'] = model_to_dict(Shop.objects.get(id=shop_id))
    except Shop.DoesNotExist:
        raise Http404('找不到商户')
    return render(request, 'dish.html', ctx)
