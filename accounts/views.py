
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from carts.views import _cart_id
from carts.models import Cart, CartItem

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid(): #       q tiene todos los campos llenos
            first_name = form.cleaned_data['first_name'] ## fetch values del request
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0] #tomar la primera parte del email para el username

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registro exitoso, cuenta creada :)')
            return redirect('register')

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)
# Create your views here.
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Listo! ya ingresaste')
            return redirect('dashboard')
        else:
            messages.error(request, 'Email o Contraseña incorrectos')
            return redirect('login')

    return render(request, 'accounts/login.html')



@login_required(login_url='login') #se tiene que haber iniciado sesion para poder cerrarla
def logout(request):
    auth.logout(request)
    messages.success(request, 'Tu sesión ha sido cerrada')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'store/store.html')
