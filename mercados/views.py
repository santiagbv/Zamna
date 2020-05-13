from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import  render
from .logic.logic_productos import get_all_productos, get_products_by_name
from .logic.logic_categoria import get_all_categorias, get_categorias_by_name
from django.core import serializers
from Zamna.auth0backend import getLogins, get_correo
from django.contrib.auth.decorators import login_required
from .forms import FirstTimeUser
from .logic.logic_usuario import create_usuario, get_usuario_correo

def index(request):
    return HttpResponse("Hello, world. You're at the mercados index.")


def get_all_products(request):
    productos = get_all_productos()
    productos_list = serializers.serialize('json', productos)
    return HttpResponse(productos_list, content_type='application/json')


def get_product_name(request, name):
    try:
        print(name)
        productos = get_products_by_name(name)

        productos_list = serializers.serialize('json', productos)
        return HttpResponse(productos_list, content_type='application/json')
    except:
        return HttpResponse('paila socito')


@login_required()
def profile(request):
    try:
        correo = get_correo(request)
        usuario = get_usuario_correo(correo)
        print(usuario)
        return render(request, 'user.html')
    except Exception as e:
        print(e)
        return usuario_create(request)



@login_required()
def usuario_create(request):
    if request.method == 'POST':
        print('hey')
        form = FirstTimeUser(request.POST)
        if form.is_valid():
            correo = get_correo(request)
            print(correo)
            create_usuario(form, correo)
            return profile(request)
        else:
            print(form.errors)
    else:
        form = FirstTimeUser()
        print(form.fields)

    context = {
        'form': form
    }
    return render(request, 'firstTimeUser.html', context)


@login_required()
def product_searched(request):
    name = request.GET.get('searching')
    productos = get_products_by_name(name)
    context ={'productos' : productos}
    return render(request, 'user.html', context)


@login_required()
def basket(request):
    return render(request, 'basket.html')
