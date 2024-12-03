from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cookie_token.auth_class import CookieJWTAuthentication
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product, Cart, CartItem
from .serializers import CartItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = []
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def retrieve(self, request, *args, **kwargs):
        # get the cart of the current user
        user = request.user
        cart = get_object_or_404(Cart, user=user, is_paid=False)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class AddToCartView(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        user = request.user
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity', 1)

        if product.stock < int(quantity):
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create cart for the user
        cart, created = Cart.objects.get_or_create(user=user, is_paid=False)

        # Get or create cart item
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += int(quantity)
        else:
            cart_item.quantity = int(quantity)

        product.stock -= int(quantity)
        product.save()

        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        user = request.user
        cart = get_object_or_404(Cart, user=user, is_paid=False)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        product = cart_item.product
        cart_item.delete()

        product.stock += cart_item.quantity
        product.save()


        return Response(status=status.HTTP_204_NO_CONTENT)


class PayCartView(APIView):

    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user, is_paid=False)
        cart.is_paid = True
        cart.delete()
        cart = Cart.objects.create(user=user)
        cart.save()
        return Response(status=status.HTTP_200_OK)