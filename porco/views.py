from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm, ProductForm
from .models import Product


class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        # Autenticar o usuário
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def get_success_url(self):
        # Redirecionar para a página desejada após o login bem-sucedido
        return reverse('lista-de-produtos')


def product_list(request):
    query = request.GET.get('search', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query) | Q(color__icontains=query)
    )
    return render(request, 'product_list.html', {'products': products})


def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)

    # Recupere o carrinho da sessão ou crie um novo se ainda não existir
    cart = request.session.get('cart', {})

    # Recupere a quantidade do produto que o cliente deseja adicionar (você deve obter isso do formulário)
    quantity_str = request.POST.get('quantity', '1').replace(',', '.')  # Substitui vírgulas por pontos
    quantity = float(quantity_str)

    # Verifique se o produto já está no carrinho
    if product_id in cart:
        # Se o produto já estiver no carrinho, atualize a quantidade
        cart[product_id]['quantity'] += quantity
    else:
        # Caso contrário, adicione o produto ao carrinho com a quantidade especificada
        cart[product_id] = {
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'quantity': quantity
        }

    # Atualize a sessão do carrinho
    request.session['cart'] = cart

    # Dispare o evento 'cartUpdated' após adicionar um item ao carrinho
    request.session.modified = True  # Certifique-se de que a sessão seja atualizada
    return redirect('lista-de-produtos')


def cart_count(request):
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return JsonResponse({'count': count})


def remove_from_cart(request, product_id):
    if 'cart' in request.session:
        cart = request.session['cart']
        if str(product_id) in cart:
            del cart[str(product_id)]
            request.session['cart'] = cart

            # Dispare o evento 'cartUpdated' após remover um item do carrinho
            request.session.modified = True  # Certifique-se de que a sessão seja atualizada

    # Redirecionar de volta para a página do carrinho
    return redirect('carrinho-de-compras')


def cart(request):
    cart = request.session.get('cart', {})
    return render(request, 'carrinho_de_compras.html', {'cart': cart})


def select_color(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Processar a seleção do usuário
            selected_color = form.cleaned_data['color']
            # Faça algo com a seleção, como salvar no banco de dados
    else:
        form = ProductForm()

    return render(request, 'select_color.html', {'form': form})
