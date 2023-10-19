from django.urls import path
from .views import CustomLoginView, product_list, add_to_cart, cart, remove_from_cart, cart_count

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('produtos/', product_list, name='lista-de-produtos'),
    path('adicionar-ao-carrinho/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remover-do-carrinho/<int:product_id>/', remove_from_cart, name='remove-from-cart'),
    path('carrinho/count/', cart_count, name='cart-count'),
    path('carrinho/', cart, name='carrinho-de-compras')
]
